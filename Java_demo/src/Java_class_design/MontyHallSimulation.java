package Java_class_design;
import javax.swing.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.text.DecimalFormat;

public class MontyHallSimulation extends JFrame {
    private JTextField inputField;
    private JButton confirmButton;
    private JTextArea resultArea;

    public MontyHallSimulation() {
        setTitle("Card Game Simulation");
        setSize(400, 300);
        setDefaultCloseOperation(EXIT_ON_CLOSE);

        JPanel mainPanel = new JPanel();
        inputField = new JTextField(10);

        confirmButton = new JButton("确认");
        resultArea = new JTextArea(10, 30);

        confirmButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                try {
                    int input = Integer.parseInt(inputField.getText());
                    simulate(input);
                } catch (NumberFormatException ex) {
                    resultArea.setText("请输入有效的整数次数");
                }
            }
        });

        mainPanel.add(new JLabel("请输入模拟次数："));
        mainPanel.add(inputField);
        mainPanel.add(confirmButton);
        mainPanel.add(resultArea);
        add(mainPanel);

        setVisible(true);
    }

    private void simulate(int trials) {
        int staySuccess = 0, switchSuccess = 0, randomSuccess = 0;
        for (int i = 0; i < trials; i++) {
            if (playStay()) staySuccess++;
            if (playSwitch()) switchSuccess++;
            if (playRandom()) randomSuccess++;
        }

        DecimalFormat df = new DecimalFormat("#.00");
        resultArea.setText(String.format("方法1，抽中金卡的次数为 %d，抽中金卡的概率为 %s%%\n", staySuccess, df.format(((double) staySuccess / trials) * 100)));
        resultArea.append(String.format("方法2，抽中金卡的次数为 %d，抽中金卡的概率为 %s%%\n", switchSuccess, df.format(((double) switchSuccess / trials) * 100)));
        resultArea.append(String.format("方法3，抽中金卡的次数为 %d，抽中金卡的概率为 %s%%", randomSuccess, df.format(((double) randomSuccess / trials) * 100)));
    }

    private boolean playStay() {
        int chosenCard = (int) (Math.random() * 3); // 0, 1, or 2
        return chosenCard == 1; // Since the gold card is always at index 1
    }

    private boolean playSwitch() {
        int chosenCard = (int) (Math.random() * 2); // 0 or 1
        return chosenCard == 0; // Since the gold card is at index 0 after switching
    }

    private boolean playRandom() {
        int chosenCard = (int) (Math.random() * 3); // 0, 1, or 2
        return chosenCard != 1; // The non-chosen silver card is revealed, so picking the other one means success.
    }

    public static void main(String[] args) {
        new MontyHallSimulation();
    }
}