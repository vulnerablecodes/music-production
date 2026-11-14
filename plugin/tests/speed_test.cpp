// Targeted Speed regression: real audio at each ratio, changed while Speed stays engaged.
#include "../src/VintageMilitaryRadio.cpp"
#include <fstream>
#include <iostream>
int main(){
 VintageMilitaryRadio p;p.prepare(48000,128);p.set(Speed,1);p.set(Noise,0);p.set(Mix,100);p.set(Bypass,0);p.reset();
 float l[128],r[128],o[128],q[128];const float* in[]={l,r};float* out[]={o,q};
 mpc::ProcessContext c;c.inputs=in;c.outputs=out;c.numInputs=c.numOutputs=2;c.numFrames=128;c.sampleRate=48000;
 const int order[]={1,0,2,3};long n=0;
 for(int index:order){p.set(SpeedMode,float(index));std::ofstream f("build/speedcheck-"+std::to_string(index)+".f32",std::ios::binary);
  for(int block=0;block<1500;++block){for(int i=0;i<128;++i){l[i]=r[i]=.3f*std::sin(float(n++)*d::kTwoPi*1000/48000);}p.process(c);f.write(reinterpret_cast<char*>(o),sizeof(o));}
  if(!p.getBool(Speed)||p.getInt(SpeedMode)!=index)return 1;
 }
 std::cout<<"PASS: Speed remains engaged while UI-order indices 1,0,2,3 are selected live\n";
}
