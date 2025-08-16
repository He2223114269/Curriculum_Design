package Java_class_design;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.Random;

public class MonteCarloSimulation extends JFrame {
    private JTextField inputTextField, outputTextField;
    private JButton simulateButton, clearButton;
    private JPanel visualizationPanel;

    public MonteCarloSimulation() {
        // 设置窗口标题和布局
        setTitle("蒙特卡洛模拟求解");
        setLayout(new BorderLayout());

        // 创建输入组件
        JLabel inputLabel = new JLabel("请输入仿真值大小：");
        inputTextField = new JTextField(10);
        simulateButton = new JButton("确认");
        clearButton = new JButton("清除");
        outputTextField = new JTextField(20);

        // 创建输入面板并添加组件
        JPanel inputPanel = new JPanel();
        inputPanel.add(inputLabel);
        inputPanel.add(inputTextField);
        inputPanel.add(simulateButton);
        inputPanel.add(clearButton);

        // 将输入面板添加到窗口顶部
        add(inputPanel, BorderLayout.NORTH);

        // 创建可视化面板
        visualizationPanel = new JPanel() {
            @Override
            protected void paintComponent(Graphics g) {
                super.paintComponent(g);
                int width = getWidth();
                int height = getHeight();

                // 绘制一个正方形
                g.drawRect(50, 50, 200, 200);

                Random rand = new Random();
                int n = Integer.parseInt(inputTextField.getText());
                int insideCircle = 0;

                for (int i = 0; i < n; i++) {
                    double x = rand.nextDouble();
                    double y = rand.nextDouble();
                    if (x * x + y * y <= 1.0) {
                        insideCircle++;
                        g.setColor(Color.RED);
                    } else {
                        g.setColor(Color.BLUE);
                    }
                    int pointX = 50 + (int) (x * 200);
                    int pointY = 250 - (int) (y * 200);
                    g.fillRect(pointX, pointY, 2, 2);
                }

                // 计算π的值
                double pi = 4.0 * insideCircle / n;
                outputTextField.setText("计算得π值为：" + pi);
            }
        };
        visualizationPanel.setBorder(BorderFactory.createTitledBorder("模拟结果可视化"));
        add(visualizationPanel, BorderLayout.CENTER);

        // 使输出文本框不可编辑并将其添加到窗口底部
        outputTextField.setEditable(false);
        add(outputTextField, BorderLayout.SOUTH);

        // 为确认和清除按钮添加动作监听器
        simulateButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                try {
                    int n = Integer.parseInt(inputTextField.getText().trim());
                    if (n <= 0) {
                        throw new IllegalArgumentException("请输入大于0的整数");
                    }
                    visualizationPanel.repaint();
                } catch (NumberFormatException ex) {
                    outputTextField.setText("请输入有效整数");
                } catch (IllegalArgumentException ex) {
                    outputTextField.setText(ex.getMessage());
                }
            }
        });

        clearButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                inputTextField.setText("");
                outputTextField.setText("");
                visualizationPanel.repaint();
            }
        });

        // 设置窗口大小、关闭操作并显示窗口
        setSize(400, 400);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setVisible(true);
    }

    public static void main(String[] args) {
        new MonteCarloSimulation();
    }
}