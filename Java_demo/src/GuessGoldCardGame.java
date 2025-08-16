import javax.swing.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.Random;

public class GuessGoldCardGame extends JFrame {
    private JTextField inputField;
    private JTextArea outputArea;

    public GuessGoldCardGame() {
        super("湖南经视台猜“黄金卡”节目");

        JLabel inputLabel = new JLabel("请输入模拟次数:");
        inputField = new JTextField(10);
        JButton simulateButton = new JButton("模拟");
        outputArea = new JTextArea(10, 20);

        simulateButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                int simulations = 0;

                try {
                    simulations = Integer.parseInt(inputField.getText());
                } catch (NumberFormatException ex) {
                    outputArea.setText("请输入有效整数！");
                    return;
                }

                int firstScenarioWins = simulateFirstScenario(simulations);
                int secondScenarioWins = simulateSecondScenario(simulations);
                int thirdScenarioWins = simulateThirdScenario(simulations);

                double firstScenarioProbability = (double) firstScenarioWins / simulations * 100;
                double secondScenarioProbability = (double) secondScenarioWins / simulations * 100;
                double thirdScenarioProbability = (double) thirdScenarioWins / simulations * 100;

                outputArea.setText("第一种方案抽中金卡的次数：" + firstScenarioWins + "，概率为：" + String.format("%.4f", firstScenarioProbability) + "%\n"
                        + "第二种方案抽中金卡的次数：" + secondScenarioWins + "，概率为：" + String.format("%.4f", secondScenarioProbability) + "%\n"
                        + "第三种方案抽中金卡的次数：" + thirdScenarioWins + "，概率为：" + String.format("%.4f", thirdScenarioProbability) + "%");
            }
        });

        JPanel panel = new JPanel();
        panel.add(inputLabel);
        panel.add(inputField);
        panel.add(simulateButton);
        panel.add(outputArea);

        add(panel);
        setSize(400, 300);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setVisible(true);
    }

    private int simulateFirstScenario(int simulations) {
        int wins = 0;
        Random random = new Random();
        for (int i = 0; i < simulations; i++) {
            int chosenCard = random.nextInt(3);
            if (chosenCard == 0) {
                wins++;
            }
        }
        return wins;
    }

    private int simulateSecondScenario(int simulations) {
        int wins = 0;
        Random random = new Random();
        for (int i = 0; i < simulations; i++) {
            int chosenCard = random.nextInt(2);
            if (chosenCard == 0) {
                wins++;
            }
        }
        return wins;
    }

    private int simulateThirdScenario(int simulations) {
        int wins = 0;
        Random random = new Random();
        for (int i = 0; i < simulations; i++) {
            int firstChoice = random.nextInt(3);
            if (firstChoice != 1) { // If not the middle card
                wins++;
            }
        }
        return wins;
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(new Runnable() {
            @Override
            public void run() {
                new GuessGoldCardGame();
            }
        });
    }
}