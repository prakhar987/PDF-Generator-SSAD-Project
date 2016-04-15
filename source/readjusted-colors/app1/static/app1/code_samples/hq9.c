#include<stdio.h>
#include<string.h>
int main()
{
	char c[101];
	scanf("%s",c);
	int l=strlen(c),i,d=0;
	for(i=0;i<l;i++)
		if(c[i]=='H'||c[i]=='Q'||c[i]=='9')
		{
			printf("YES\n");
			d=1;
			break;
		}
	if(d==0)
		printf("NO\n");
	return 0;
}
