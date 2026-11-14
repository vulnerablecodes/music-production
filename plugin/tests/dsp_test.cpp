// Direct DSP tests supplement the SDK ABI/state/automation host simulator.
#include "../src/VintageMilitaryRadio.cpp"
#include <iostream>
#include <fstream>
#include <stdexcept>
static void require(bool b,const char* msg){if(!b)throw std::runtime_error(msg);}
static void defaults(VintageMilitaryRadio& p){for(int i=0;i<p.numParams();++i)p.set(i,p.param(i).def);}
int main(){
 try{
 VintageMilitaryRadio p;
 float l[512],r[512],ol[512],orr[512];const float* in[]={l,r};float* out[]={ol,orr};
 mpc::ProcessContext ctx;ctx.inputs=in;ctx.outputs=out;ctx.numInputs=ctx.numOutputs=2;ctx.transport.tempoValid=true;ctx.transport.bpm=120;
 for(double sr:{44100.,48000.,96000.}){
  p.prepare(sr,512);ctx.sampleRate=sr;
  for(int block:{32,127,128,511,512}){
   ctx.numFrames=block;defaults(p);p.reset();
   for(int n=0;n<100;++n){for(int i=0;i<block;++i){l[i]=.3f*std::sin(float((n*block+i)*440*6.2831853/sr));r[i]=-.5f*l[i];}p.process(ctx);}
   // Settled wet=0 must preserve dry audio exactly, independently by channel.
   p.set(Mix,0);p.reset();p.process(ctx);
   for(int i=0;i<block;++i){require(std::abs(l[i]-ol[i])<1e-6,"dry L mismatch");require(std::abs(r[i]-orr[i])<1e-6,"dry R mismatch");}
   p.set(Bypass,1);p.set(Out,6);p.set(Mix,100);p.reset();p.process(ctx);
   for(int i=0;i<block;++i)require(std::abs(l[i]-ol[i])<1e-6,"bypass mismatch");
   // Each mode and all modes together: non-finite/unbounded output is a failure.
   for(int mode=0;mode<=8;++mode){
    defaults(p);if(mode<8)p.set(Speed+mode,1);else for(int k=Speed;k<=Stutter;++k)p.set(k,1);
    p.reset();
    for(int n=0;n<170;++n){
     for(int k=SpeedMode;k<Count;++k) if(n%17==0)p.set(k,(n/17)%2?p.param(k).min:p.param(k).max);
     for(int i=0;i<block;++i){l[i]=.5f*std::sin(float((n*block+i)*440*6.2831853/sr));r[i]=.3f*std::cos(float((n*block+i)*313*6.2831853/sr));}
     p.process(ctx);for(int i=0;i<block;++i){require(std::isfinite(ol[i])&&std::isfinite(orr[i]),"NaN/Inf");require(std::abs(ol[i])<8&&std::abs(orr[i])<8,"unbounded output");}
    }
   }
   // In-place processing must match separate buffers, including stereo reads.
   VintageMilitaryRadio a,b; a.prepare(sr,block);b.prepare(sr,block);a.set(Sat,1);b.set(Sat,1);a.reset();b.reset();
   float il[512],ir[512];for(int i=0;i<block;++i){il[i]=l[i]=i*.0002f;ir[i]=r[i]=-il[i];}
   a.process(ctx);float* inplace[]={il,ir};const float* ii[]={il,ir};ctx.inputs=ii;ctx.outputs=inplace;b.process(ctx);ctx.inputs=in;ctx.outputs=out;
   for(int i=0;i<block;++i){require(std::abs(il[i]-ol[i])<1e-6,"inplace L");require(std::abs(ir[i]-orr[i])<1e-6,"inplace R");}
  }
  std::cout<<"PASS: "<<sr<<" Hz; blocks 32,127,128,511,512; eight modes + stack, bounds, dry/bypass, in-place\n";
 }
 // Stable spectral renders: dry reference and all four speed ratios.
 ctx.numFrames=128;ctx.sampleRate=44100;p.prepare(44100,128);
 for(int rate=-1;rate<4;++rate){defaults(p);if(rate>=0){p.set(Speed,1);p.set(SpeedMode,float(rate));}p.reset();
  std::ofstream f("build/speed-"+std::to_string(rate)+".f32",std::ios::binary);
  for(int n=0;n<1034;++n){for(int i=0;i<128;++i)l[i]=r[i]=.3f*std::sin(float((n*128+i)*440*6.2831853/44100));p.process(ctx);f.write(reinterpret_cast<char*>(ol),128*sizeof(float));}
 }
 // Brake must stop and Mute must silence at fully wet (after smoothing).
 for(int mode:{Brake,Mute}){defaults(p);p.set(mode,1);p.reset();float peak=0;
  for(int n=0;n<1600;++n){for(int i=0;i<128;++i)l[i]=r[i]=.4f*std::sin(float((n*128+i)*440*6.2831853/44100));p.process(ctx);if(n>1500)for(int i=0;i<128;++i)peak=std::max(peak,std::abs(ol[i]));}
  require(peak<1e-5,mode==Brake?"brake never stops":"mute does not silence");
 }
 std::cout<<"PASS: brake stops, mute silences; speed renders written\n";
 }catch(const std::exception& e){std::cerr<<"FAIL: "<<e.what()<<"\n";return 1;}
}
