static bool min_path_bottom_up(const long long *a, size_t rows, size_t cols, PathResult *out) {
    if (!a || !out || rows == 0 || cols == 0) return false;
    size_t n = rows * cols;
    long long *dp = malloc(n * sizeof(*dp));
    unsigned char *parent = calloc(n, 1); /* 1=up, 2=left */
    if (!dp || !parent) { free(dp); free(parent); return false; }
    dp[0] = a[0];
    for (size_t j=1;j<cols;++j){dp[j]=dp[j-1]+a[j];parent[j]=2;}
    for (size_t i=1;i<rows;++i){dp[i*cols]=dp[(i-1)*cols]+a[i*cols];parent[i*cols]=1;}
    for (size_t i=1;i<rows;++i) for(size_t j=1;j<cols;++j){
        size_t k=i*cols+j; long long up=dp[k-cols], left=dp[k-1];
        if (up <= left) { dp[k]=up+a[k]; parent[k]=1; } /* tie: up */
        else { dp[k]=left+a[k]; parent[k]=2; }
    }
    size_t len=rows+cols-1;
    out->rows=malloc(len*sizeof(*out->rows)); out->cols=malloc(len*sizeof(*out->cols));
    if(!out->rows||!out->cols){free(out->rows);free(out->cols);free(dp);free(parent);return false;}
    size_t i=rows-1,j=cols-1,pos=len;
    while(pos){--pos;out->rows[pos]=i;out->cols[pos]=j;if(i==0&&j==0)break;if(parent[i*cols+j]==1)--i;else --j;}
    out->sum=dp[n-1];out->length=len;free(dp);free(parent);return true;
}
