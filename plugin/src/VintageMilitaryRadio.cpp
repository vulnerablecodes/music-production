// Vintage Military Radio — original tape-performance DSP, MIT.
// Signal flow: input -> varispeed -> reverse -> brake -> stutter -> warble
// -> saturation -> lo-fi -> hiss -> mute -> wet/dry -> output. Bypass is dry.
// Buffers allocate only in prepare(). All controls are host-automatable.
#include "mpc_plugin.h"
#include "dsp/delay_line.h"
#include "dsp/smoother.h"
#include "dsp/math.h"
#include <algorithm>
#include <array>
#include <pthread.h>
#include <time.h>
#include <atomic>
namespace d = mpc::dsp;
enum { Out, Noise, Mix, Bypass, Hold, Speed, Sat, Mute, Reverse, Warble, Lofi,
       Brake, Stutter, SpeedMode, SatMode, WarbleMode, LofiMode, BrakeMode,
       StutterMode, Drive, Depth, RevTime, Tone, NoiseTone, Edge, View, Wear, ReelPhase, Count };
class VintageMilitaryRadio : public mpc::Plugin {
public:
 VintageMilitaryRadio():Plugin(description()) {
  addParam(mpc::floatParam("output","Output",-24,6,0,"dB",1));
  addParam(mpc::floatParam("noise","Noise",0,100,0,"%",0));
  addParam(mpc::floatParam("mix","Mix",0,100,100,"%",0));
  addParam(mpc::boolParam("bypass","Bypass",false));
  addParam(mpc::boolParam("hold","Hold",true));
  const char* ids[]={"speed","sat","mute","reverse","warble","lofi","brake","stutter"};
  const char* names[]={"Speed","Saturation","Mute","Reverse","Warble","Lo-Fi","Brake","Stutter"};
  for(int i=0;i<8;++i) addParam(mpc::boolParam(ids[i],names[i],false));
  addParam(mpc::choiceParam("speed_mode","Tape Speed",{"1/2","1/4","3/4","9/10"}));
  addParam(mpc::choiceParam("sat_mode","Sat Type",{"Boost","Amp","Drive"}));
  addParam(mpc::choiceParam("warble_mode","Warble Type",{"Gentle","Wow","Flutter","Worn","Seasick","Unstable","Jungle"}));
  addParam(mpc::choiceParam("lofi_mode","Lo-Fi Type",{"Dust","Cassette","Narrow","8-bit","6-bit","4-bit","Broken","Telephone"}));
  addParam(mpc::choiceParam("brake_mode","Brake Time",{"1/8 beat","1/2 beat","1 beat","2 beats"},2));
  addParam(mpc::choiceParam("stutter_mode","Stutter Rate",{"1/2","1/4","1/8","1/16","1/32","1/64","1/8T","1/16T (old)","1/4T"},3));
  addParam(mpc::floatParam("drive","Drive",0,100,35,"%",0));
  addParam(mpc::floatParam("depth","Warble Depth",0,100,40,"%",0));
  addParam(mpc::choiceParam("reverse_time","Reverse Size",{"1/8","1/4","1/2","1 bar"},1));
  addParam(mpc::logParam("tone","Tone",500,20000,18000,"Hz",0));
  addParam(mpc::logParam("noise_tone","Hiss Tone",800,16000,7500,"Hz",0));
  addParam(mpc::floatParam("edge","Edge Fade",1,20,4,"ms",1));
  // Appended UI selector preserves every v1.0.0 parameter ID and index.
  addParam(mpc::choiceParam("view","Mode View",{"Speed","Sat","Mute","Reverse","Warble","Lo-Fi","Brake","Stutter"}));
  addParam(mpc::floatParam("repeat_wear","Repeat Wear",0,100,10,"%",0));
  // Host-polled UI telemetry: updated without allocation or host automation callbacks.
  auto reel=mpc::floatParam("reel_phase","Reel Phase",0,1,0);reel.automatable=false;addParam(reel);
  preset("Clean",{});
  preset("Dusty Deck",{{Sat,1},{Warble,1},{Lofi,1},{Noise,8},{LofiMode,1},{Mix,80}});
  preset("Half Speed",{{Speed,1},{Sat,1},{Drive,20}});
  preset("Quarter Dream",{{Speed,1},{SpeedMode,1},{Warble,1},{Depth,65},{Mix,75}});
  preset("Jungle Crunch",{{Sat,1},{SatMode,2},{Lofi,1},{LofiMode,3},{Drive,65}});
  preset("Reverse Dub",{{Reverse,1},{Sat,1},{RevTime,2},{Mix,70}});
  preset("Flutter Reel",{{Warble,1},{WarbleMode,2},{Depth,60},{Noise,5}});
  preset("Stutter 16",{{Stutter,1},{StutterMode,3}});
 }
 ~VintageMilitaryRadio() override {
  uiStop_.store(true,std::memory_order_release);
  if(uiStarted_.load(std::memory_order_acquire))pthread_join(uiThread_,nullptr);
 }
 bool formatValue(int index,float plain,std::string& out) override {
  if(index!=ReelPhase)return false;
  (void)plain;char buf[24];std::snprintf(buf,sizeof(buf),"UI %03u",uiTicks_.load(std::memory_order_relaxed)%1000);out=buf;return true;
 }
 void prepare(double sr,int) override {
  sr_=float(mpc::clamp(sr,8000.0,192000.0));
  // Per-stage history bounds: reverse needs twice the maximum 8 s chunk.
  const float history[]={.125f,16.01f,4.01f,8.01f,.04f};
  for(int k=0;k<5;++k) for(auto& ch:delay_[k]) ch.prepare(int(sr_*history[k])+8);
  for(auto& sm:smooth_) sm.setTime(4,sr_);
  reset();
  // Native skin animation owns its clock; no host-notification worker.
 }
 void reset() override {
  for(auto& stage:delay_) for(auto& ch:stage) ch.reset();
  phase_=wow_=flutter_=revAge_=brakeAge_=stutAge_=0;
  rng_=0x88cc7711; held_[0]=held_[1]=lp_[0]=lp_[1]=hp_[0]=hp_[1]=0;
  hiss_[0]=hiss_[1]=dcIn_[0]=dcIn_[1]=dcOut_[0]=dcOut_[1]=0;
  for(int k=0;k<Count;++k) smooth_[k].snap(k==Out?d::dbToGain(get(k)):get(k));
  tone_[0]=tone_[1]=0;reelPhase_=get(ReelPhase);
  for(int k=0;k<8;++k) was_[k]=false;
  sampleHold_=0; drift_=driftTarget_=0; wearState_[0]=wearState_[1]=0; loops_=0; lastStutter_=-1; lastReverse_=-1; speedRatio_=1; reverseSpan_=stutterSpan_=2; brakeDelay_=1;
 }
 void process(mpc::ProcessContext& ctx) override {
  float v[Count]; for(int k=0;k<Count;++k){v[k]=get(k);smooth_[k].setTarget(v[k]);}
  const float bpm=float(ctx.transport.tempoValid?mpc::clamp(ctx.transport.bpm,30.0,300.0):120.0);
  uiBpm_.store(bpm,std::memory_order_relaxed);
  const float beat=sr_*60/bpm;
  const float speeds[]={.5f,.25f,.75f,.9f};
  const float brakes[]={.125f,.5f,1,2}, repeats[]={2,1,.5f,.25f,.125f,.0625f,1.f/3,1.f/6,2.f/3};
  const float reverseBeats[]={.5f,1,2,4};
  const int sm=int(v[SpeedMode]), wm=int(v[WarbleMode]), lm=int(v[LofiMode]);
  const float brakeLength=beat*brakes[int(v[BrakeMode])];
  const float edge=std::max(1.f,v[Edge]*.001f*sr_);
  smooth_[Out].setTarget(d::dbToGain(v[Out]));
  const float toneCoef=1-std::exp(-d::kTwoPi*std::min(v[Tone],sr_*.45f)/sr_);
  const float hissCoef=1-std::exp(-d::kTwoPi*std::min(v[NoiseTone],sr_*.45f)/sr_);
  const float cutoffs[]={10000,6500,2600,8000,5500,3500,1800,3000};
  const int bits[]={15,12,10,8,6,4,5,10}, decim[]={1,2,3,3,4,6,10,2};
  const float lcoef=1-std::exp(-d::kTwoPi*std::min(cutoffs[lm],sr_*.4f)/sr_);
  const float quant=float(1<<(bits[lm]-1));
  const float wowRates[]={.35f,.7f,.3f,1.1f,.28f,1.7f,3.1f};
  const float flutterRates[]={5,4,9,7,3,11,15};
  const float wowDepth[]={.2f,.45f,.8f,1.2f,1.8f,2.6f,4};
  const float flutterDepth[]={.02f,.04f,.06f,.1f,.18f,.3f,.5f};
  const float grain=sr_*.12f;
  if(v[Reverse]>.5f && (!was_[3] || int(v[RevTime])!=lastReverse_)) {revAge_=0;reverseSpan_=std::min(sr_*8,beat*reverseBeats[int(v[RevTime])]);}
  if(v[Brake]>.5f && !was_[6]) {brakeAge_=0;brakeDelay_=1;}
  if(v[Stutter]>.5f && (!was_[7] || int(v[StutterMode])!=lastStutter_)) {stutAge_=0;loops_=0;wearState_[0]=wearState_[1]=0;stutterSpan_=std::max(8.f,std::min(sr_*8,beat*repeats[int(v[StutterMode])]));}
  lastStutter_=int(v[StutterMode]);lastReverse_=int(v[RevTime]);
  const float wear=v[Wear]*.01f;
  for(int k=0;k<8;++k) was_[k]=v[Speed+k]>.5f;
  for(int i=0;i<ctx.numFrames;++i){
   float a[2]={0,0};for(int c=0;c<2;++c) if(ctx.inputs && c<ctx.numInputs && ctx.inputs[c]) a[c]=ctx.inputs[c][i];
   float en[8];for(int k=0;k<8;++k) en[k]=smooth_[Speed+k].process();
   const float mix=smooth_[Mix].process()*.01f, ns=smooth_[Noise].process()*.0008f;
   const float by=smooth_[Bypass].process(), gain=smooth_[Out].process();
   const float drive=smooth_[Drive].process()*.01f, depth=smooth_[Depth].process()*.01f;
   speedRatio_+=.002f*((v[Speed]>.5f?speeds[sm]:1.f)-speedRatio_);
   phase_=d::wrapPhase(phase_+(1-speedRatio_)/grain);
   const float ph2=d::wrapPhase(phase_+.5f), w=1-std::fabs(2*phase_-1);
   wow_=d::wrapPhase(wow_+wowRates[wm]/sr_); flutter_=d::wrapPhase(flutter_+flutterRates[wm]/sr_);
   if((sampleHold_ & 127)==0)driftTarget_=random();
   drift_+=.0004f*(driftTarget_-drift_);
   const float wobble=sr_*.001f*depth*(wowDepth[wm]*d::fastSin01(wow_)+flutterDepth[wm]*d::fastSin01(flutter_)+.3f*wowDepth[wm]*drift_);
   const float brakeSpeed=std::max(0.f,1-brakeAge_/brakeLength);
   if(v[Brake]>.5f){brakeAge_+=1;brakeDelay_+=1-brakeSpeed;}
   // Drive the UI from the same motor ratio as the audio. Freeze on stopped transport.
   float motor=by>.5f?1.f:speedRatio_;
   if(by<.5f && v[Reverse]>.5f)motor=-motor;
   if(by<.5f && v[Brake]>.5f)motor*=brakeSpeed;
   if(!ctx.transport.valid || ctx.transport.playing)reelPhase_=d::wrapPhase(reelPhase_+motor*.9f/sr_);
   const bool latch=v[Stutter]>.5f;
   const bool updateHeld=(sampleHold_++%decim[lm])==0;
   for(int c=0;c<2;++c){
    float x=a[c];
    delay_[0][c].write(x);
    float shifted=delay_[0][c].readLinear(1+phase_*grain)*w+delay_[0][c].readLinear(1+ph2*grain)*(1-w);
    x+=en[0]*(shifted-x);
    delay_[1][c].write(x);
    // Backward chunks from previously received audio, never from future input.
    const float rev=delay_[1][c].readLinear(2+2*revAge_)*edgeWindow(revAge_,reverseSpan_,edge);
    x+=en[3]*(rev-x);
    delay_[2][c].write(x);
    float br=delay_[2][c].readLinear(std::min(sr_*8,brakeDelay_))*std::min(1.f,brakeSpeed*20);
    x+=en[6]*(br-x);
    // Freeze the stutter history while engaged; release resumes live capture.
    if(!latch) delay_[3][c].write(x);
    float st=delay_[3][c].readLinear(stutterSpan_-stutAge_);
    // Optional original wear: repeated passes progressively narrow and quantize.
    const float age=std::min(100.f,float(loops_))*wear;
    wearState_[c]+=(1.f/(1.f+age*.7f))*(st-wearState_[c]);
    const float q=float(1 << std::max(4,16-int(age*.7f)));
    const float worn=std::round(wearState_[c]*q)/q/(1.f+age*.08f);
    st=(wear>0?worn:st)*edgeWindow(stutAge_,stutterSpan_,edge);
    x+=en[7]*(st-x);
    delay_[4][c].write(x);
    const float wa=delay_[4][c].readLinear(sr_*.008f+wobble);
    x+=en[4]*(wa-x);
    float saturated;
    if(int(v[SatMode])==0) saturated=d::softClip(x*(1+drive*2));
    else if(int(v[SatMode])==1) saturated=(d::fastTanh(x*(1+drive*7)+.12f)-d::fastTanh(.12f))*.9f;
    else saturated=d::fastTanh(x*(1+drive*18))*.85f;
    x+=en[1]*(saturated-x);
    lp_[c]+=lcoef*(x-lp_[c]);
    if(updateHeld) held_[c]=std::round(lp_[c]*quant)/quant;
    hp_[c]+=.03f*(held_[c]-hp_[c]);
    float lo=lm==7?held_[c]-hp_[c]:held_[c];
    if(lm==6) lo*=std::fabs(d::fastSin01(wow_))>.15f?1.f:.25f;
    x+=en[5]*(lo-x);
    hiss_[c]+=hissCoef*(random()-hiss_[c]);
    x+=hiss_[c]*(ns+(en[5]*(lm==0?.0008f:.0002f)));
    x*=1-en[2];
    // Tone is only applied to wet audio. DC blocker removes asymmetric drive DC.
    tone_[c]+=toneCoef*(x-tone_[c]); x=tone_[c];
    const float dc=x-dcIn_[c]+.995f*dcOut_[c];dcIn_[c]=x;dcOut_[c]=dc;
    float wet=a[c]+mix*(dc-a[c]);
    wet=wet*gain; // Output gain is downstream of mix; bypass returns unity dry.
    const float out=wet+by*(a[c]-wet);
    if(c<ctx.numOutputs) ctx.outputs[c][i]=out;
   }
   if(v[Reverse]>.5f) {revAge_+=1;if(revAge_>=reverseSpan_)revAge_=0;}
   if(latch){stutAge_+=1;if(stutAge_>=stutterSpan_){stutAge_=0;loops_=std::min(10000,loops_+1);}}
  }
  // UI worker owns ReelPhase and notifies the host; no host calls in process().
 }
private:
 // A real-time-safe boundary: the audio thread never calls the host for painting.
 // This follows the OpenMPC worker-notification pattern; no UpdateDisplay screen rebuilds.
 static double uiNow() {timespec t{};clock_gettime(CLOCK_MONOTONIC,&t);return double(t.tv_sec)+double(t.tv_nsec)*1e-9;}
 static void* uiEntry(void* arg) {static_cast<VintageMilitaryRadio*>(arg)->uiLoop();return nullptr;}
 void startUiClock() {
  if(!host_ || !effect_ || uiStarted_.load(std::memory_order_acquire))return;
  pthread_attr_t attr;pthread_attr_init(&attr);
  sched_param priority{};
  int ok=pthread_attr_setinheritsched(&attr,PTHREAD_EXPLICIT_SCHED);
  ok|=pthread_attr_setschedpolicy(&attr,SCHED_OTHER);
  ok|=pthread_attr_setschedparam(&attr,&priority);
  if(ok==0 && pthread_create(&uiThread_,&attr,&uiEntry,this)==0)uiStarted_.store(true,std::memory_order_release);
  pthread_attr_destroy(&attr);
 }
 void uiLoop() {
  double previous=uiNow(),phase=0,brakeAge=0;int lastFrame=-1;bool wasBrake=false;
  constexpr float rates[]={.5f,.25f,.75f,.9f};constexpr float brakeBeats[]={.125f,.5f,1.f,2.f};
  while(!uiStop_.load(std::memory_order_acquire)) {
   timespec pause{0,40000000};nanosleep(&pause,nullptr); // 25 Hz, normal OS priority.
   if(uiStop_.load(std::memory_order_acquire))break;
   const double now=uiNow(),dt=mpc::clamp(now-previous,0.0,.2);previous=now;
   const bool brake=getBool(Brake);
   if(brake && !wasBrake)brakeAge=0;
   wasBrake=brake;
   float motor=getBool(Speed)&&!getBool(Bypass)?rates[getInt(SpeedMode)]:0.f;
   if(getBool(Reverse))motor=-motor;
   if(brake){brakeAge+=dt;const double duration=60.0/uiBpm_.load(std::memory_order_relaxed)*brakeBeats[getInt(BrakeMode)];motor*=float(std::max(0.0,1.0-brakeAge/duration));}
   phase+=dt*.9*motor;phase-=std::floor(phase);
   const int frame=mpc::clamp(int(phase*64),0,63);
   if(frame!=lastFrame) {
    setNormalised(ReelPhase,float(frame)/63.f);
    // audioMasterAutomate informs MPC's cached value model; it is NOT called from process().
    // Reel Phase is non-automatable, excluded from user controls and Q-Link maps.
    notifyHostParameterChanged(ReelPhase);
    uiTicks_.fetch_add(1,std::memory_order_relaxed);lastFrame=frame;
   }
  }
 }
 pthread_t uiThread_{};std::atomic<bool> uiStop_{false},uiStarted_{false};
 std::atomic<unsigned> uiTicks_{0};std::atomic<float> uiBpm_{120.f};
 static mpc::PluginInfo description(){mpc::PluginInfo i;i.name="Vintage Military Radio";i.vendor="Tropix R!X Crazy Jungle Sounds";i.uniqueId=MPC_FOURCC('V','M','R','8');i.version=1011;i.isInstrument=false;i.numInputs=2;i.numOutputs=2;i.wantsMidi=false;i.tailSamples=0;return i;}
 void preset(const char* name,std::initializer_list<std::pair<int,float>> edits){std::vector<float> v;for(int k=0;k<numParams();++k)v.push_back(param(k).def);for(auto e:edits)v[e.first]=e.second;addProgram(name,v);}
 static float edgeWindow(float pos,float len,float edge){edge=std::min(edge,len*.2f);return std::min(1.f,std::min(pos/edge,(len-pos)/edge));}
 float random(){rng_^=rng_<<13;rng_^=rng_>>17;rng_^=rng_<<5;return float(int32_t(rng_))*(1.f/2147483648.f);}
 std::array<std::array<d::DelayLine,2>,5> delay_;
 std::array<d::Smoother,Count> smooth_;
 float sr_=44100,phase_=0,wow_=0,flutter_=0,revAge_=0,reverseSpan_=2,brakeAge_=0,brakeDelay_=1,stutAge_=0,stutterSpan_=2,speedRatio_=1;
 float held_[2]={},lp_[2]={},hp_[2]={},hiss_[2]={},tone_[2]={},dcIn_[2]={},dcOut_[2]={};
 float reelPhase_=0;
 float drift_=0,driftTarget_=0,wearState_[2]={};int loops_=0,lastStutter_=-1,lastReverse_=-1;
 uint32_t rng_=0x88cc7711,sampleHold_=0;bool was_[8]={};
};
MPC_PLUGIN_ENTRY(VintageMilitaryRadio)
