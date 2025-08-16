package Java_class_design;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

public class SimpleCalculator extends JFrame {
    private JTextField inputField;
    private JTextField resultField;
    private String inputString = "";
    private boolean isNewCalculation = true;

    public SimpleCalculator() {
        setTitle("简单计算器");
        setLayout(new GridLayout(2, 1));

        inputField = new JTextField();
        inputField.setEditable(false);
        add(inputField);

        resultField = new JTextField();
        resultField.setEditable(false);
        add(resultField);

        JPanel buttonPanel = new JPanel(new GridLayout(4, 4));

        String[] buttonLabels = {
                "7", "8", "9", "/",
                "4", "5", "6", "*",
                "1", "2", "3", "-",
                "0", ".", "=", "+"
        };

        for (String buttonLabel : buttonLabels) {
            JButton button = new JButton(buttonLabel);
            button.addActionListener(new ButtonClickListener());
            buttonPanel.add(button);
        }
        add(buttonPanel);

        setSize(300, 400);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setVisible(true);
    }

    private void updateInputField(String text) {
        if (isNewCalculation) {
            inputString = "";
            isNewCalculation = false;
        }
        inputString += text;
        inputField.setText(inputString);
    }

    private void calculateResult() {
        String expression = inputString;
        // 利用你的计算逻辑进行计算，并将结果放入resultField中
        // 在这个示例中，我们只做基本的字符串解析来实现加减乘除运算，需要你进一步完善
        String result = "0"; // 这里存放计算结果
        resultField.setText(result);
    }

    private class ButtonClickListener implements ActionListener {
        public void actionPerformed(ActionEvent e) {
            String command = e.getActionCommand();
            if (command.equals("=")) {
                calculateResult();
                isNewCalculation = true;
            } else if (command.equals("C")) {
                inputString = "";
                inputField.setText("");
                isNewCalculation = true;
            } else {
                updateInputField(command);
            }
        }
    }

    public static void main(String[] args) {
        new SimpleCalculator();
    }
}