package Java_class_design;


import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JTextField;
import java.awt.FlowLayout;
import java.awt.Color;
import java.awt.Container;
import java.awt.Dimension;
import java.awt.Font;
import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;
public class computer extends JFrame {
    computer() {
        // 设置窗口标题为"简易计算器"
        super("简易计算器");
        // 创建字体对象f，字体为"黑体"，大小为30
        Font f = new Font("黑体", 30, 30);
        // 创建两个文本输入框对象jt1和jt2
        JTextField jt1 = new JTextField(null);
        JTextField jt2 = new JTextField(null);
        jt1.setFont(f);
        jt2.setFont(f);
        // 将文本输入框对象jt1和jt2中的文本内容设置为右对齐
        jt1.setHorizontalAlignment(JTextField.RIGHT);
        jt2.setHorizontalAlignment(JTextField.RIGHT);
        // 获取窗口的内容面板对象，并将布局设置为左对齐的流式布局，组件之间水平间距为5，垂直间距为5
        Container c = getContentPane();
        c.setLayout(new FlowLayout(FlowLayout.LEFT, 5, 5));
        // 将文本输入框对象jt1和jt2添加到内容面板对象c中
        c.add(jt1);
        c.add(jt2);
        // 设置文本输入框 jt1 和 jt2 的尺寸
        jt1.setPreferredSize(new Dimension(370, 70));
        jt2.setPreferredSize(new Dimension(370, 75));
        // 设置文本输入框 jt1 和 jt2 为不可编辑状态
        jt1.setEditable(false);
        jt2.setEditable(false);
        // 创建一个包含16个 JButton 对象的数组
        JButton jb[] = new JButton[16];
        for (int j = 0; j < 16; j++) {
            //创建一个新的 JButton 对象。
            jb[j] = new JButton();
            //将按钮的背景颜色设置为白色。
            jb[j].setBackground(Color.WHITE);
            //设置按钮的焦点为非可聚焦状态。
            jb[j].setFocusable(false);
            //设置按钮的尺寸为 90x90 像素。
            jb[j].setPreferredSize(new Dimension(90, 90));
            //将按钮的字体设置为前面定义的字体对象 f。
            jb[j].setFont(f);
            //将按钮添加到容器 c 中。
            c.add(jb[j]);
        }
        //设置窗口为不可改变大小的。
        this.setResizable(false);
        //对各个按钮的名称赋值
        jb[0].setText("+");
        jb[1].setText("-");
        jb[2].setText("*");
        jb[3].setText("/");
        jb[4].setText("1");
        jb[5].setText("2");
        jb[6].setText("3");
        jb[7].setText("C");
        //将 jb 数组中索引为 7 的元素的背景颜色设置为橙色。
        jb[7].setBackground(Color.ORANGE);
        jb[8].setText("4");
        jb[9].setText("5");
        jb[10].setText("6");
        jb[11].setText("0");
        jb[12].setText("7");
        jb[13].setText("8");
        jb[14].setText("9");
        jb[15].setText("=");
        //创建了一个 JButton 数组，名为 Button_num
        JButton Button_num[] = {
                jb[4],
                jb[5],
                jb[6],
                jb[8],
                jb[9],
                jb[10],
                jb[11],
                jb[12],
                jb[13],
                jb[14]
        };
        //遍历 Button_num 数组，并为每个按钮添加了一个 ActionListener。
        // 当按钮被点击时，将其文本追加到 jt2 的文本框中。
        for (int i = 0; i < Button_num.length; i++) {
            Button_num[i].addActionListener(new ActionListener() {
                public void actionPerformed(ActionEvent e) {
                    JButton action_Button = (JButton) e.getSource();
                    jt2.setText(jt2.getText() + action_Button.getText());
                }
            });
        }
        //循环给按钮数组 jb 的前 4 个按钮分别添加 ActionListener。
        // 当按钮被点击时，它会检查 jt2 文本框中最后一个字符，
        // 如果是加号、减号、乘号或除号之一，则禁用该按钮，
        // 否则将 jt2 的文本设置为点击的按钮的文本。
        for (int j = 0; j < 4; j++) {
            jb[j].addActionListener(new ActionListener() {
                public void actionPerformed(ActionEvent e) {
                    String s = jt2.getText();
                    char ch = s.charAt(s.length() - 1);

                    if (ch == '+' || ch == '-' || ch == '*' || ch == '/')((JButton) e.getSource()).setEnabled(false);
                    else {
                        jt1.setText(jt2.getText());
                        jt2.setText(((JButton) e.getSource()).getText());
                    }

                }
            });
        }
        //为 jb 数组中索引为 7 的按钮添加了一个 ActionListener。
        //当这个按钮被点击时，会清空 jt1 和 jt2 的文本内容
        jb[7].addActionListener(new ActionListener() {
                                    public void actionPerformed(ActionEvent e) {
                                        jt1.setText(null);
                                        jt2.setText(null);
                                    }
                                }
        );
        //为 jb 数组中索引为 15 的按钮添加了一个 ActionListener。当这个按钮被点击时，
        // 它会尝试计算 jt1 和 jt2 文本框中的内容，然后根据计算结果更新 jt1 和 jt2 的文本内容。
        // 如果出现算术异常，它会将 jt1 清空，并在 jt2 中显示 "ERROR"。
        jb[15].addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                try {
                    String Calculate_String = jt1.getText() + jt2.getText();
                    int result = calculation.result(Calculate_String);
                    jt1.setText(null);
                    jt2.setText(Integer.toString(result));
                } catch(ArithmeticException ex) {
                    jt1.setText(null);
                    jt2.setText("ERROR");
                }
            }
        }
        );
    }

    public static void main(String args[]) {
        computer app = new computer();
        //设置了在关闭窗口时默认的操作，这里是设置为退出程序。
        app.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        app.setSize(400, 580);
        //显示窗口
        app.setVisible(true);
    }
}

