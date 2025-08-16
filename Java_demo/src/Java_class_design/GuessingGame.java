package Java_class_design;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.Random;

public class GuessingGame {
    public static void main(String[] args) {
        SwingUtilities.invokeLater(new Runnable() {
            public void run() {
                GuessingGameUI gameUI = new GuessingGameUI();
                gameUI.launchGame();
            }
        });
    }
}

class GuessingGameUI extends JFrame {
    private JButton card1Button, card2Button, card3Button, confirmButton, restartButton, exitButton;
    private JLabel resultLabel;
    private JPanel buttonPanel, resultPanel;

    public GuessingGameUI() {
        setTitle("湖南经视台猜“黄金卡”节目");

        card1Button = new JButton("卡1");
        card1Button.setActionCommand("1");
        card2Button = new JButton("卡2");
        card2Button.setActionCommand("2");
        card3Button = new JButton("卡3");
        card3Button.setActionCommand("3");

        confirmButton = new JButton("确认");
        restartButton = new JButton("重新开始");
        exitButton = new JButton("退出游戏");

        resultLabel = new JLabel("", JLabel.CENTER);

        buttonPanel = new JPanel();
        resultPanel = new JPanel();
    }

    public void launchGame() {
        buttonPanel.setLayout(new FlowLayout());
        buttonPanel.add(card1Button);
        buttonPanel.add(card2Button);
        buttonPanel.add(card3Button);
        buttonPanel.add(confirmButton);

        setLayout(new BorderLayout());
        add(buttonPanel, BorderLayout.NORTH);
        add(resultLabel, BorderLayout.CENTER);

        confirmButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                handleSelection(e.getActionCommand());
            }
        });

        restartButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                restartGame();
            }
        });

        exitButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                System.exit(0);
            }
        });

        setSize(400, 200);
        setVisible(true);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
    }

    private void handleSelection(String selectedCard) {
        Random random = new Random();
        int goldCard = random.nextInt(3) + 1;

        if (Integer.parseInt(selectedCard) == goldCard) {
            resultLabel.setText("您选择的卡为：金卡");
        } else {
            resultLabel.setText("您选择的卡为：银卡");
        }

        confirmButton.setEnabled(false); // 禁用确认按钮
        add(resultPanel, BorderLayout.SOUTH); // 将结果面板添加到界面
        resultPanel.add(restartButton);
        resultPanel.add(exitButton);
    }

    private void restartGame() {
        resultPanel.remove(restartButton);
        resultPanel.remove(exitButton);
        resultPanel.setVisible(false);
        confirmButton.setEnabled(true); // 重新启用确认按钮
        resultLabel.setText(""); // 清空结果
    }
}