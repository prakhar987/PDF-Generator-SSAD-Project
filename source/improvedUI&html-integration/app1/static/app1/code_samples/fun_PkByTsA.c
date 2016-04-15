#include<stdio.h>
/*long long int merge(long long int a[],long long int low,long long int mid,long long int high)
{
	long long int l,i,m,temp[high+1],k;
	i=low;
	l=low;
	m=mid+1;
	while(l<=mid && m<=high)
		if(a[l]<=a[m])
			temp[i++]=a[l++];
		else
			temp[i++]=a[m++];
	if(l>mid)
		for(k=m;k<=high;k++)
			temp[i++]=a[k];
	else
		for(k=l;k<=mid;k++)
			temp[i++]=a[k];
	for(k=low;k<=high;k++)
		a[k]=temp[k];

}
long long int part(long long int a[],long long int low,long long int high)
{
	long long int mid;
	if(low<high)
	{
		mid=(low+high)/2;
		part(a,low,mid);
		part(a,mid+1,high);
		merge(a,low,mid,high);
	}
}*/
int main()
{
	long long int n;
	scanf("%lld",&n);
	long long int a[n],i;
	for(i=0;i<n;i++)
		scanf("%lld",&a[i]);
//	part(a,0,n-1);
	long long int sum=0;
	for(i=0;i<n-2;i++)
		sum+=a[i];
	printf("%lld\n",sum*a[n-1]);
	return 0;
}

