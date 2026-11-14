// Measure UI phase against audio time, not wall clock or a fixed GUI timer.
#include "../src/VintageMilitaryRadio.cpp"
#include <iostream>
#include <stdexcept>
int main(){try{
 VintageMilitaryRadio p;p.prepare(48000,128);float z[128]={},l[128],r[128];const float* in[]={z,z};float* out[]={l,r};mpc::ProcessContext c;c.inputs=in;c.outputs=out;c.numInputs=c.numOutputs=2;c.numFrames=128;c.sampleRate=48000;c.transport.valid=true;c.transport.playing=true;c.transport.tempoValid=true;c.transport.bpm=120;
 auto run=[&](int blocks){float total=0,last=p.get(ReelPhase);for(int n=0;n<blocks;++n){p.process(c);float now=p.get(ReelPhase),diff=now-last;if(diff<-.5f)diff+=1;if(diff>.5f)diff-=1;total+=diff;last=now;}return total;};
 const float expected[]={.45f,.225f,.675f,.81f};
 for(int i:{1,0,2,3}){p.set(Speed,1);p.set(SpeedMode,float(i));p.reset();run(375);float rate=run(750)/2; if(std::abs(rate-expected[i])>.0003f)throw std::runtime_error("reel speed ratio mismatch");std::cout<<"PASS speed index "<<i<<": "<<rate<<" reel revolutions/sec\n";}
 c.transport.playing=false;if(std::abs(run(100))>1e-7)throw std::runtime_error("reels move while stopped");std::cout<<"PASS stopped transport freezes reels\n";
 c.transport.playing=true;p.set(Reverse,1);run(375);if(run(375)>=0)throw std::runtime_error("reverse reels go forward");std::cout<<"PASS reverse rotates backward\n";
 p.set(Reverse,0);p.set(Brake,1);p.set(BrakeMode,2);run(750);if(std::abs(run(100))>1e-7)throw std::runtime_error("brake does not stop reels");std::cout<<"PASS brake stops reels\n";
 if(p.param(ReelPhase).automatable)throw std::runtime_error("phase telemetry automatable");
 }catch(const std::exception& e){std::cerr<<"FAIL: "<<e.what()<<"\n";return 1;}}
