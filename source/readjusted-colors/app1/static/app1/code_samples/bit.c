#include<stdio.h>
int main()
{
	int n,i,c1=0;
	scanf("%d",&n);
	char a1,a2,a3,c;
	c=getchar();
	for(i=0;i<n;i++)
	{
		scanf("%c%c%c",&a1,&a2,&a3);
	//	printf("%c%c%c\n",a1,a2,a3);
		if(a2=='-')
			c1--;
		else
			c1++;
		scanf("%c",&c);
	}
	printf("%d\n",c1);
	return 0;
}
