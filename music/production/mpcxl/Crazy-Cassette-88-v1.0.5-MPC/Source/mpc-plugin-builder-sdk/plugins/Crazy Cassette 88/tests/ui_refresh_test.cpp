// Reproduce MPC-style cached picture state: only host notifications refresh it.
#include "../src/CrazyCassette88.cpp"
#include <iostream>
#include <stdexcept>
#include <thread>
#include <chrono>
std::atomic<float> cached{0};std::atomic<unsigned> calls{0},updates{0},badAudioCalls{0};
thread_local bool audioThread=false;
static VstIntPtr host(AEffect*,VstInt32 op,VstInt32 index,VstIntPtr,void*,float value){
 if(op==audioMasterVersion)return 2400;
 if(op==audioMasterUpdateDisplay)updates.fetch_add(1);
 if(op==audioMasterAutomate){if(audioThread)badAudioCalls.fetch_add(1);if(index!=ReelPhase)throw std::runtime_error("worker writes a user control");cached.store(value);calls.fetch_add(1);}
 return 0;
}
static void req(bool ok,const char* msg){if(!ok)throw std::runtime_error(msg);}
int main(){try{
 auto* e=VSTPluginMain(host);req(e!=nullptr,"create failed");auto* p=static_cast<CrazyCassette88*>(e->object);
 e->dispatcher(e,effSetSampleRate,0,0,nullptr,48000);e->dispatcher(e,effSetBlockSize,0,128,nullptr,0);e->dispatcher(e,effMainsChanged,0,1,nullptr,0);
 p->set(Speed,1);p->set(Bypass,0);
 float z[128]={},l[128],r[128];float* in[]={z,z};float* out[]={l,r};
 const float ratios[]={.5f,.25f,.75f,.9f};
 for(int index:{1,0,2,3}){
  p->set(SpeedMode,float(index));std::this_thread::sleep_for(std::chrono::milliseconds(120));
  float last=cached.load(),rotations=0;auto start=std::chrono::steady_clock::now();unsigned before=calls.load();
  for(int tick=0;tick<100;++tick){audioThread=true;e->processReplacing(e,in,out,128);audioThread=false;std::this_thread::sleep_for(std::chrono::milliseconds(20));float now=cached.load(),d=now-last;if(d<-.5f)d+=1;if(d>.5f)d-=1;rotations+=d;last=now;}
  double secs=std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();float rate=rotations/float(secs);req(calls.load()-before>10,"cached picture receives no continuous changes");req(std::abs(rate-ratios[index]*.9f)<.07f,"reported frame speed mismatch");
  std::cout<<"PASS host-cache animation speed index "<<index<<": "<<rate<<" rev/s, "<<calls.load()-before<<" notifications without screen taps\n";
 }
 req(badAudioCalls.load()==0,"callback from audio thread");req(updates.load()==0,"full screen rebuild callback sent");
 p->set(Speed,0);std::this_thread::sleep_for(std::chrono::milliseconds(100));unsigned stopped=calls.load();std::this_thread::sleep_for(std::chrono::milliseconds(160));req(calls.load()==stopped,"motion persists after Speed off");
 req(e->dispatcher(e,effCanBeAutomated,ReelPhase,0,nullptr,0)==0,"display parameter automatable");
 std::cout<<"PASS: no UI gesture or transport required; callbacks only off audio thread; no UpdateDisplay; stationary when disabled\n";
 e->dispatcher(e,effMainsChanged,0,0,nullptr,0);e->dispatcher(e,effClose,0,0,nullptr,0);unsigned closed=calls.load();std::this_thread::sleep_for(std::chrono::milliseconds(100));req(calls.load()==closed,"callback after destruction");
 std::cout<<"PASS: worker joined before plugin closes; no use-after-close notification\n";
 }catch(const std::exception& e){std::cerr<<"FAIL: "<<e.what()<<"\n";return 1;}}
