package Java_class_design;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

// "猜黄金卡"游戏程序
public class GuessGoldCardGame extends JFrame {
    private JButton card1, card2, card3, confirm, restart, exit;
    private JLabel resultLabel;
    private boolean goldCard;

    // 构造函数
    public GuessGoldCardGame() {
        setTitle("湖南经视台猜“黄金卡”节目"); // 设置窗口标题
        setSize(300, 200); // 设置窗口大小
        setDefaultCloseOperation(EXIT_ON_CLOSE); // 设置关闭操作
        setLayout(new FlowLayout()); // 设置布局为流式布局

        // 初始化按钮和标签
        card1 = new JButton("卡1");
        card2 = new JButton("卡2");
        card3 = new JButton("卡3");
        confirm = new JButton("确认");
        resultLabel = new JLabel();

        // 将组件添加到窗口
        add(card1);
        add(card2);
        add(card3);
        add(confirm);
        add(resultLabel);

        // 为按钮添加动作监听器
        card1.addActionListener(new CardListener());
        card2.addActionListener(new CardListener());
        card3.addActionListener(new CardListener());
        confirm.addActionListener(new ConfirmListener());

        // 初始化并为重新开始和退出按钮添加动作监听器
        restart = new JButton("重新开始");
        exit = new JButton("退出游戏");
        restart.addActionListener(e -> resetGame());
        exit.addActionListener(e -> System.exit(0));
    }

    // 卡按钮的动作监听器
    private class CardListener implements ActionListener {
        public void actionPerformed(ActionEvent e) {
            if (e.getSource() == card1) {
                card1.setEnabled(false);
                card2.setEnabled(true);
                card3.setEnabled(true);
                goldCard = false; // 假设卡1是银卡
            } else if (e.getSource() == card2) {
                card1.setEnabled(true);
                card2.setEnabled(false);
                card3.setEnabled(true);
                goldCard = false; // 假设卡2是银卡
            } else if (e.getSource() == card3) {
                card1.setEnabled(true);
                card2.setEnabled(true);
                card3.setEnabled(false);
                goldCard = true; // 假设卡3是金卡
            }
        }
    }

    // 确认按钮的动作监听器
    private class ConfirmListener implements ActionListener {
        public void actionPerformed(ActionEvent e) {
            if (goldCard) {
                resultLabel.setText("您选择的卡为：金卡"); // 显示结果：选择了金卡
            } else {
                resultLabel.setText("您选择的卡为：银卡"); // 显示结果：选择了银卡
            }
            add(restart); // 添加重新开始按钮
            add(exit); // 添加退出按钮
            validate(); // 验证窗口
        }
    }

    // 重置游戏
    private void resetGame() {
        card1.setEnabled(true);
        card2.setEnabled(true);
        card3.setEnabled(true);
        resultLabel.setText(""); // 清空结果标签
        remove(restart); // 移除重新开始按钮
        remove(exit); // 移除退出按钮
        validate(); // 验证窗口
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> new GuessGoldCardGame().setVisible(true)); // 创建并显示游戏窗口
    }
}