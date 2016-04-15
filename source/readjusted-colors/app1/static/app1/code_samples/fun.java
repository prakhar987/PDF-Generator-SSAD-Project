import java.util.Arrays;
import java.util.Scanner;
class fun
{
	public static void main(String arg[])
	{
		String s;
		int i = 1;
		Scanner in = new Scanner(System.in);
		String A=in.next();
		String B=in.next();
		int a=A.length();
		int b=B.length();
		System.out.println(a+b);
		int a1=0,b1=0,x1,y1,flag = 0;
		char x,y;
		while(a1<a && b1<b){
			x = A.charAt(a1);
			y = B.charAt(b1);
			x1 = (int)x;
			y1 = (int)y;
			if(x1<y1){
				flag = 1;
				break;
			}
			a1 += 1;
			b1 += 1;
		}
		if(a<b)
			flag = 1;
		if(flag==0)
			System.out.println("YES");
		else
			System.out.println("NO");
		char w[] = A.toCharArray();
		char d[] = B.toCharArray();
		x1 = (int)w[0];
		x1 -= 32;
		w[0] = (char)x1;
		x1 = (int)d[0];
		x1 -= 32;
		d[0] = (char)x1;
		x1 = 0;
		while(x1<a)
		{
			System.out.print(w[x1]);
			x1 += 1;
		}
		System.out.print(" ");
		x1 = 0;
		while(x1<b)
		{
			System.out.print(d[x1]);
			x1 += 1;
		}
		System.out.print("\n");
	}
}