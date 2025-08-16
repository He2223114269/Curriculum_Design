package Java_class_design;

import javax.swing.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.ArrayList;
import java.util.List;



public class TextSegmentationApp extends JFrame {

    private JButton segmentButton, clearButton;
    private JTextField inputField;
    private JTextArea resultArea;

    public TextSegmentationApp() {
        setTitle("文本分词"); // 设置窗体标题
        setSize(400, 300); // 设置窗体尺寸
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE); // 设置窗体关闭行为
        setLayout(null); // 设置布局为绝对布局

        inputField = new JTextField(); // 创建文本输入框
        inputField.setBounds(20, 20, 250, 30); // 设置位置和尺寸
        add(inputField); // 将文本输入框添加到窗体

        segmentButton = new JButton("确认"); // 创建确认按钮
        segmentButton.setBounds(280, 20, 80, 30); // 设置位置和尺寸
        add(segmentButton); // 将确认按钮添加到窗体

        resultArea = new JTextArea(); // 创建文本区域
        resultArea.setBounds(20, 70, 340, 150); // 设置位置和尺寸
        add(resultArea); // 将文本区域添加到窗体

        clearButton = new JButton("清除"); // 创建清除按钮
        clearButton.setBounds(150, 230, 100, 30); // 设置位置和尺寸
        add(clearButton); // 将清除按钮添加到窗体

        // 为确认按钮添加事件监听器，处理文本分词
        segmentButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                segmentText();
            }
        });

        // 为清除按钮添加事件监听器，清空文本域和输入框
        clearButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                clearFields();
            }
        });
    }

    // 文本分词处理
    private void segmentText() {
        try {
            String inputText = inputField.getText(); // 获取输入文本
            if (inputText.isEmpty()) { // 如果输入文本为空则显示提示信息
                JOptionPane.showMessageDialog(this, "请输入文本");
                return;
            }
            List<String> segmentedText = performSegmentation(inputText); // 执行分词处理
            resultArea.setText(""); // 清空文本区
            for (String segment : segmentedText) {
                resultArea.append(segment + "\n"); // 分词结果显示在文本区域
            }
        } catch (Exception ex) {
            // 异常处理，显示异常信息
            JOptionPane.showMessageDialog(this, "分词过程中发生异常：" + ex.getMessage());
        }
    }

    // 执行分词处理
    private List<String> performSegmentation(String input) {
        List<String> result = new ArrayList<>(); // 创建结果列表
        StringBuilder sb = new StringBuilder(); // 创建字符串构建器
        for (int i = 0; i < input.length(); i++) {
            char c = input.charAt(i);
            // 判断是否为中文字符
            if (isChinese(c)) {
                if (sb.length() > 0) {
                    result.add(sb.toString());
                    sb.setLength(0);
                }
                result.add(String.valueOf(c));
            } else {
                // 判断是否为英文字符
                if (isEnglish(c)) {
                    sb.append(c);
                } else {
                    if (sb.length() > 0) {
                        result.add(sb.toString());
                        sb.setLength(0);
                    }
                }
            }
        }
        if (sb.length() > 0) {
            result.add(sb.toString());
        }
        return result;
    }

    // 判断字符是否为中文
    private boolean isChinese(char c) {
        return c >= 0x4E00 && c <= 0x9FA5;
    }

    // 判断字符是否为英文
    private boolean isEnglish(char c) {
        return (c >= 'A' && c <= 'Z') || (c >= 'a' && c <= 'z');
    }

    // 清空输入框和文本域
    private void clearFields() {
        inputField.setText("");
        resultArea.setText("");
    }

    // 主方法，创建应用实例并设置可见性
    public static void main(String[] args) {
        SwingUtilities.invokeLater(new Runnable() {
            @Override
            public void run() {
                TextSegmentationApp app = new TextSegmentationApp();
                app.setVisible(true);
            }
        });
    }
}