package Java_class_design;

//再定义一个计算类calculation.java:
public class calculation {
    calculation() {};
    boolean is_operator(char ch) {
        if (ch == '+' || ch == '-' || ch == '*' || ch == '/') return true;
        else return false;
    }
    static int result(String s) {
        String ch[] = {
                "+",
                "-",
                "*",
                "/"
        };
        // 提取第一个和第二个操作数
        int i = 0;
        int index;
        // 找到第一个运算符的索引
        while (s.indexOf(ch[i]) == -1 && i < 4) {
            i++;
        }
        // 如果找不到运算符，则返回-1
        if (i == 4) return - 1;

        else index = s.indexOf(ch[i]);

        // 提取第一个和第二个操作数
        String s1 = s.substring(0, index);
        String s2 = s.substring(index + 1, s.length());
        // 根据运算符计算结果
        if (i == 0) return Integer.parseInt(s1) + Integer.parseInt(s2);
        if (i == 1) return Integer.parseInt(s1) - Integer.parseInt(s2);
        if (i == 2) return Integer.parseInt(s1) * Integer.parseInt(s2);
        if (i == 3 && Integer.parseInt(s2) != 0) return Integer.parseInt(s1) / Integer.parseInt(s2);
        else if (i == 3 && Integer.parseInt(s2) == 0) {
            throw new ArithmeticException();// 如果除数为0，则抛出算术异常
        }
        return - 1;// 如果出现错误，则返回-1
    }

}

