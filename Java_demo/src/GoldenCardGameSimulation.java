import javax.swing.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.Random;

public class GoldenCardGameSimulation extends JFrame {
    private JTextField inputField;
    private JTextArea outputArea;

    public GoldenCardGameSimulation() {
        setTitle("湖南经视台猜“黄金卡”节目");
        setSize(400, 300);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        JPanel panel = new JPanel();
        inputField = new JTextField(10);
        inputField.setToolTipText("请输入模拟游戏的次数");
        JButton simulateButton = new JButton("模拟游戏");
        outputArea = new JTextArea(10, 30);
        outputArea.setEditable(false);

        simulateButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                simulateGames();
            }
        });

        panel.add(new JLabel("输入模拟次数："));
        panel.add(inputField);
        panel.add(simulateButton);
        panel.add(new JScrollPane(outputArea));

        add(panel);
        setVisible(true);
    }

    private void simulateGames() {
        outputArea.setText("");

        try {
            int totalSimulations = Integer.parseInt(inputField.getText());
            int firstScenarioWins = 0, secondScenarioWins = 0, thirdScenarioWins = 0;

            Random random = new Random();

            for (int i = 0; i < totalSimulations; i++) {
                // 第一种情况
                if (random.nextInt(3) == 0) {
                    firstScenarioWins++;
                }
                // 第二种情况
                if (random.nextBoolean()) {
                    secondScenarioWins++;
                }
                // 第三种情况
                int chosenCard = random.nextInt(3);
                if (chosenCard != 0) {
                    thirdScenarioWins++;
                }
            }

            outputArea.append(String.format("第一种方案抽中金卡的次数：%d，概率为%.4f%%\n", firstScenarioWins, ((double)firstScenarioWins / totalSimulations) * 100));
            outputArea.append(String.format("第二种方案抽中金卡的次数：%d，概率为%.4f%%\n", secondScenarioWins, ((double)secondScenarioWins / totalSimulations) * 100));
            outputArea.append(String.format("第三种方案抽中金卡的次数：%d，概率为%.4f%%\n", thirdScenarioWins, ((double)thirdScenarioWins / totalSimulations) * 100));

        } catch (NumberFormatException e) {
            outputArea.setText("请输入一个有效的整数！");
        }
    }

    public static void main(String[] args) {
        new GoldenCardGameSimulation();
    }
}