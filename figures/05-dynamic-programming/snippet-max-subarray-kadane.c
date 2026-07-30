static bool max_subarray_kadane(const long long *a,size_t n,MaxSubarrayResult *out){
    if(!a||!out||n==0)return false;
    MaxSubarrayResult ending={a[0],0,0},best=ending;
    for(size_t i=1;i<n;++i){
        MaxSubarrayResult extend={ending.sum+a[i],ending.start,i},restart={a[i],i,i};
        ending=better(restart,extend)?restart:extend;if(better(ending,best))best=ending;
    }*out=best;return true;
}
