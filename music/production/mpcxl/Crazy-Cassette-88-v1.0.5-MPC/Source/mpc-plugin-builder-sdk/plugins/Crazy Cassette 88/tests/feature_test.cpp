// Verify that every visible character setting drives distinct audio, not UI-only stubs.
#include "../src/CrazyCassette88.cpp"
#include <iostream>
#include <stdexcept>
#include <vector>
static void req(bool b,const char* s){if(!b)throw std::runtime_error(s);}
int main(){try{
 CrazyCassette88 p;p.prepare(48000,128);
 float l[128],r[128],o[128],q[128];const float* in[]={l,r};float* out[]={o,q};
 mpc::ProcessContext c;c.inputs=in;c.outputs=out;c.numInputs=c.numOutputs=2;c.numFrames=128;c.sampleRate=48000;c.transport.tempoValid=true;c.transport.bpm=120;
 auto defaults=[&](){for(int k=0;k<p.numParams();++k)p.set(k,p.param(k).def);};
 auto signal=[&](int t){for(int i=0;i<128;++i){float n=float(t*128+i);l[i]=r[i]=.25f*std::sin(n*.0521f)+.16f*std::sin(n*.149f)+.08f*std::sin(n*n*.0000009f);}};
 const int params[]={SpeedMode,SatMode,-1,-1,WarbleMode,LofiMode,BrakeMode,StutterMode};
 const std::vector<int> settings[]={{0,1,2,3},{1,0,2},{0},{0},{0,1,2,3,4,5,6},{0,1,2,3,4,5,6,7},{0,1,2,3},{0,1,8,2,6,3,4,5}};
 int count=0;
 for(int mode=0;mode<8;++mode){std::vector<float> previous;
  for(int setting:settings[mode]){defaults();p.reset();for(int t=0;t<400;++t){signal(t);p.process(c);} // fill live history before engagement
   if(params[mode]>=0)p.set(params[mode],float(setting));p.set(Speed+mode,1);
   std::vector<float> rendered;rendered.reserve(128*450);
   for(int t=400;t<850;++t){signal(t);p.process(c);for(float v:o){req(std::isfinite(v),"non-finite character output");rendered.push_back(v);}}
   if(!previous.empty()){double diff=0;for(size_t i=0;i<rendered.size();++i)diff+=std::abs(rendered[i]-previous[i]);req(diff/rendered.size()>1e-5,"two character variants produce identical audio");}
   previous=rendered;++count;
  }
  std::cout<<"PASS mode "<<mode+1<<": "<<settings[mode].size()<<" visible settings drive audio\n";
 }
 // Changing selected UI view must not engage effects or alter the audio result.
 defaults();p.reset();signal(0);p.process(c);float expected[128];std::copy(o,o+128,expected);
 for(int view=0;view<8;++view){defaults();p.set(View,float(view));p.reset();signal(0);p.process(c);for(int i=0;i<128;++i)req(std::abs(expected[i]-o[i])<1e-7,"view changes audio");for(int k=Speed;k<=Stutter;++k)req(!p.getBool(k),"view enables an effect");}
 std::cout<<"PASS: "<<count<<" documented character settings; all 8 view selections leave sound and enables unchanged\n";
 // Independent hiss: audible with no modes enabled; completely absent at dry mix.
 defaults();p.set(Noise,100);p.reset();for(int i=0;i<128;++i)l[i]=r[i]=0;p.process(c);double n=0;for(float v:o)n+=v*v;req(n>1e-5,"noise fader inactive");p.set(Mix,0);p.reset();p.process(c);for(float v:o)req(v==0,"noise leaks through dry mix");
 std::cout<<"PASS independent Noise and Mix behavior\n";
 const char* ids[]={"output","noise","mix","bypass","hold","speed","sat","mute","reverse","warble","lofi","brake","stutter","speed_mode","sat_mode","warble_mode","lofi_mode","brake_mode","stutter_mode","drive","depth","reverse_time","tone","noise_tone","edge"};
 for(int i=0;i<25;++i)req(p.param(i).id==ids[i],"legacy parameter ID/index changed");
 // Build a v1.0.0-style chunk: 25 parameters, old eight-choice stutter range.
 defaults();std::vector<uint8_t> state={'M','P','C','P'};
 auto u32=[&](uint32_t x){for(int j=0;j<4;++j)state.push_back(uint8_t(x>>(j*8)));};
 auto f32=[&](float x){uint32_t bits;std::memcpy(&bits,&x,4);u32(bits);};
 u32(2);u32(25);
 for(int i=0;i<25;++i){auto id=p.param(i).id;state.push_back(uint8_t(id.size()));for(char a:id)state.push_back(uint8_t(a));float plain=i==StutterMode?7.f:p.param(i).def;f32(plain);f32(i==StutterMode?1.f:p.param(i).toNormalised(plain));}
 u32(0);req(p.internalLoadState(state.data(),state.size()),"legacy chunk rejected");req(p.getInt(StutterMode)==7,"legacy stutter division changed");
 std::cout<<"PASS original 25 stable IDs/indices and legacy 1/16T state restoration\n";

}catch(const std::exception& e){std::cerr<<"FAIL "<<e.what()<<"\n";return 1;}}
