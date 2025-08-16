package Mypackage;                     //声明存放类的包
import java.util.*;                          //引用 java.util 包
public class KY6_1 {
    private int year,month,day;
    public static void main(String[] args){}
    public KY6_1 (int y,int m,int d) {
        year = y;
        month = (((m>=1) & (m<=12)) ? m : 1);
        day = (((d>=1) & (d<=31)) ? d : 1);
    }
    public static int thisyear() {
        return Calendar.getInstance().get(Calendar.YEAR);//返回当年的年份
    }
    public int year() {
        return year;//返回年份
    }
    public String toString(){
        return year+"-"+month+"-"+day;//返回转化为字符串的年-月-日
    }
}
