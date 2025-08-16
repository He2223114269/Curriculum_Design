package Mypackage;

// 创建第一个接口，包含一个抽象方法用于完成两个数的加法操作
interface Adder {
    abstract int add(int a, int b);
}

// 创建第二个接口，包含一个抽象方法用于完成两个数的减法操作
interface Subtractor {
    abstract int subtract(int a, int b);
}

// 创建一个类KY6_3来实现上述两个接口中的抽象方法
public class KY6_3 implements Adder, Subtractor {
    @Override
    public int add(int a, int b) {
        return a + b;
    }

    @Override
    public int subtract(int a, int b) {
        return a - b;
    }
    public static void main(String[] args) {
        KY6_3 adder = new KY6_3();
        int result1 = adder.add(2, 3);
        System.out.println("2 + 3 = " + result1);

        int result2 = adder.subtract(5, 2);
        System.out.println("5 - 2 = " + result2);
    }
}