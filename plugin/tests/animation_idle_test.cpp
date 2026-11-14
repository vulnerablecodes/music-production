#include "mpc_vst2_abi.h"
#include <dlfcn.h>
#include <atomic>
#include <chrono>
#include <thread>
#include <set>
#include <cassert>
#include <iostream>
std::atomic<int> notices{0};
VstIntPtr host(AEffect*,VstInt32 op,VstInt32 idx,VstIntPtr,void*,float){if(op==audioMasterVersion)return 2400;if(op==audioMasterAutomate&&idx==27)++notices;return 0;}
int main(int argc,char**argv){assert(argc==2);void*lib=dlopen(argv[1],RTLD_NOW);assert(lib);auto entry=(AEffect*(*)(audioMasterCallback))dlsym(lib,"VSTPluginMain");assert(entry);auto e=entry(host);assert(e);auto call=[&](int op,int v=0,float opt=0){return e->dispatcher(e,op,0,v,nullptr,opt);};
call(effOpen);call(effSetSampleRate,0,44100);call(effSetBlockSize,128);call(effMainsChanged,1);
std::set<int> frames;for(int i=0;i<10;++i){std::this_thread::sleep_for(std::chrono::milliseconds(55));frames.insert(int(e->getParameter(e,27)*63+.5f));}assert(frames.size()>=8);assert(notices>=8);std::cout<<"PASS default Speed OFF: "<<frames.size()<<" distinct idle frames; "<<notices<<" host notifications, without calling processReplacing\n";
e->setParameter(e,3,1);int before=notices;std::this_thread::sleep_for(std::chrono::milliseconds(200));assert(notices>before);std::cout<<"PASS bypass: animation continues\n";
call(effMainsChanged,0);call(effMainsChanged,1);before=notices;std::this_thread::sleep_for(std::chrono::milliseconds(200));assert(notices>before);std::cout<<"PASS suspend/resume: animation continues\n";
call(effMainsChanged,0);call(effClose);before=notices;std::this_thread::sleep_for(std::chrono::milliseconds(100));assert(notices==before);dlclose(lib);std::cout<<"PASS close: worker joined, no callbacks after teardown\n";}
