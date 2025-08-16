package Java_class_design;

import java.awt.BasicStroke;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.Graphics2D;
/*
 * CirclePiTest.java
 *
 * Created on __DATE__, __TIME__
 */
/**
 *
 * @author  __USER__
 */
public class Test3 extends javax.swing.JApplet {
    /** Initializes the applet CirclePiTest */
    public String testnumstr, innumstr, totalnumstr, resultstr;
    public double myRandom(double b) {
        double t = Math.random();
        t = t * b;
        return t;
    }
    public double getPi(double a) {
        int i, j = 0;
        double t1, t2;
        for (i = 0; i < a; i++) {
            t1 = myRandom(20);
            t2 = myRandom(20);
            if (t1 * t1 + t2 * t2 < 400) {
                j++;
            }
        }
        a = j * 4 / a;
        return a;
    }
    public void paint(java.awt.Graphics g) {
        super.paint(g);
        Dimension d = DrawPane.getSize();
        java.awt.Graphics cg = DrawPane.getGraphics();
        BasicStroke stoke = new BasicStroke(3);
        Graphics2D cg2d = (Graphics2D) cg;
        cg2d.setStroke(stoke);
        cg2d.setColor(new Color(172, 22, 172));
        cg2d.drawLine(20, d.height - 20, d.width, d.height - 20);
        cg2d.drawLine(20, 20, 20, d.height - 20);
        cg2d.drawLine(20, d.height / 3, d.width * 2 / 3, d.height / 3);
        cg2d.drawLine(d.width * 2 / 3, d.height / 3, d.width * 2 / 3,
                d.height - 20);
        cg2d.setColor(new Color(22, 172, 172));
        cg2d.fillArc(20 - (d.width * 2 / 3 - 20), d.height / 3,
                (d.width * 2 / 3 - 20) * 2, (d.height * 2 / 3 - 20) * 2, 0, 90);
    }
    public void init() {
        try {
            java.awt.EventQueue.invokeAndWait(new Runnable() {
                public void run() {
                    initComponents();
                }
            });
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }
    //GEN-BEGIN:initComponents
    // <editor-fold defaultstate="collapsed" desc="Generated Code">
    private void initComponents() {
        jLabel1 = new javax.swing.JLabel();
        totaltestnum = new javax.swing.JTextField();
        jLabel2 = new javax.swing.JLabel();
        totalrunnum = new javax.swing.JTextField();
        jLabel4 = new javax.swing.JLabel();
        resultnum = new javax.swing.JTextField();
        DrawPane = new javax.swing.JPanel();
        jButton1 = new javax.swing.JButton();
        jLabel1.setText("\u8bf7\u8f93\u5165\u8bd5\u9a8c\u6b21\u6570:count=");
        jLabel2.setText("\u603b\u7684\u91c7\u6837\u6570\uff1an=");
        jLabel4.setText("\u5706\u5468\u7387\u03c0\uff1a");
        resultnum.setEditable(false);
        javax.swing.GroupLayout DrawPaneLayout = new javax.swing.GroupLayout(
                DrawPane);
        DrawPane.setLayout(DrawPaneLayout);
        DrawPaneLayout.setHorizontalGroup(DrawPaneLayout.createParallelGroup(
                javax.swing.GroupLayout.Alignment.LEADING).addGap(0, 218,
                Short.MAX_VALUE));
        DrawPaneLayout.setVerticalGroup(DrawPaneLayout.createParallelGroup(
                javax.swing.GroupLayout.Alignment.LEADING).addGap(0, 210,
                Short.MAX_VALUE));
        jButton1.setText("\u8ba1\u7b97");
        jButton1.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                jButton1ActionPerformed(evt);
            }
        });
        javax.swing.GroupLayout layout = new javax.swing.GroupLayout(
                getContentPane());
        getContentPane().setLayout(layout);
        layout.setHorizontalGroup(layout
                .createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                .addGroup(
                        layout.createSequentialGroup()
                                .addGroup(
                                        layout.createParallelGroup(
                                                javax.swing.GroupLayout.Alignment.LEADING,
                                                false)
                                                .addGroup(
                                                        layout.createSequentialGroup()
                                                                .addContainerGap()
                                                                .addGroup(
                                                                        layout.createParallelGroup(
                                                                                javax.swing.GroupLayout.Alignment.TRAILING)
                                                                                .addGroup(
                                                                                        layout.createSequentialGroup()
                                                                                                .addComponent(
                                                                                                        jLabel2,
                                                                                                        javax.swing.GroupLayout.PREFERRED_SIZE,
                                                                                                        96,
                                                                                                        javax.swing.GroupLayout.PREFERRED_SIZE)
                                                                                                .addPreferredGap(
                                                                                                        javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                                                                                                .addComponent(
                                                                                                        totalrunnum,
                                                                                                        javax.swing.GroupLayout.PREFERRED_SIZE,
                                                                                                        92,
                                                                                                        javax.swing.GroupLayout.PREFERRED_SIZE))
                                                                                .addGroup(
                                                                                        layout.createSequentialGroup()
                                                                                                .addComponent(
                                                                                                        jLabel1,
                                                                                                        javax.swing.GroupLayout.PREFERRED_SIZE,
                                                                                                        133,
                                                                                                        javax.swing.GroupLayout.PREFERRED_SIZE)
                                                                                                .addPreferredGap(
                                                                                                        javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                                                                                                .addComponent(
                                                                                                        totaltestnum,
                                                                                                        javax.swing.GroupLayout.PREFERRED_SIZE,
                                                                                                        56,
                                                                                                        javax.swing.GroupLayout.PREFERRED_SIZE))
                                                                                .addGroup(
                                                                                        layout.createSequentialGroup()
                                                                                                .addComponent(
                                                                                                        jLabel4)
                                                                                                .addPreferredGap(
                                                                                                        javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                                                                                                .addComponent(
                                                                                                        resultnum,
                                                                                                        javax.swing.GroupLayout.PREFERRED_SIZE,
                                                                                                        114,
                                                                                                        javax.swing.GroupLayout.PREFERRED_SIZE)
                                                                                                .addPreferredGap(
                                                                                                        javax.swing.LayoutStyle.ComponentPlacement.RELATED)))
                                                                .addGap(18, 18,
                                                                        18))
                                                .addGroup(
                                                        javax.swing.GroupLayout.Alignment.TRAILING,
                                                        layout.createSequentialGroup()
                                                                .addContainerGap(
                                                                        javax.swing.GroupLayout.DEFAULT_SIZE,
                                                                        Short.MAX_VALUE)
                                                                .addComponent(
                                                                        jButton1,
                                                                        javax.swing.GroupLayout.PREFERRED_SIZE,
                                                                        78,
                                                                        javax.swing.GroupLayout.PREFERRED_SIZE)
                                                                .addGap(67, 67,
                                                                        67)))
                                .addComponent(DrawPane,
                                        javax.swing.GroupLayout.PREFERRED_SIZE,
                                        javax.swing.GroupLayout.DEFAULT_SIZE,
                                        javax.swing.GroupLayout.PREFERRED_SIZE)
                                .addGap(74, 74, 74)));
        layout.setVerticalGroup(layout
                .createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                .addGroup(
                        layout.createSequentialGroup()
                                .addContainerGap()
                                .addGroup(
                                        layout.createParallelGroup(
                                                javax.swing.GroupLayout.Alignment.LEADING)
                                                .addGroup(
                                                        layout.createSequentialGroup()
                                                                .addGroup(
                                                                        layout.createParallelGroup(
                                                                                javax.swing.GroupLayout.Alignment.BASELINE)
                                                                                .addComponent(
                                                                                        totaltestnum,
                                                                                        javax.swing.GroupLayout.DEFAULT_SIZE,
                                                                                        29,
                                                                                        Short.MAX_VALUE)
                                                                                .addComponent(
                                                                                        jLabel1,
                                                                                        javax.swing.GroupLayout.PREFERRED_SIZE,
                                                                                        29,
                                                                                        javax.swing.GroupLayout.PREFERRED_SIZE))
                                                                .addGap(18, 18,
                                                                        18)
                                                                .addGroup(
                                                                        layout.createParallelGroup(
                                                                                javax.swing.GroupLayout.Alignment.BASELINE)
                                                                                .addComponent(
                                                                                        jLabel2,
                                                                                        javax.swing.GroupLayout.PREFERRED_SIZE,
                                                                                        27,
                                                                                        javax.swing.GroupLayout.PREFERRED_SIZE)
                                                                                .addComponent(
                                                                                        totalrunnum,
                                                                                        javax.swing.GroupLayout.DEFAULT_SIZE,
                                                                                        29,
                                                                                        Short.MAX_VALUE))
                                                                .addPreferredGap(
                                                                        javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
                                                                .addGroup(
                                                                        layout.createParallelGroup(
                                                                                javax.swing.GroupLayout.Alignment.BASELINE)
                                                                                .addComponent(
                                                                                        jLabel4,
                                                                                        javax.swing.GroupLayout.PREFERRED_SIZE,
                                                                                        27,
                                                                                        javax.swing.GroupLayout.PREFERRED_SIZE)
                                                                                .addComponent(
                                                                                        resultnum,
                                                                                        javax.swing.GroupLayout.DEFAULT_SIZE,
                                                                                        29,
                                                                                        Short.MAX_VALUE))
                                                                .addGap(49, 49,
                                                                        49)
                                                                .addComponent(
                                                                        jButton1,
                                                                        javax.swing.GroupLayout.PREFERRED_SIZE,
                                                                        42,
                                                                        javax.swing.GroupLayout.PREFERRED_SIZE))
                                                .addComponent(
                                                        DrawPane,
                                                        javax.swing.GroupLayout.PREFERRED_SIZE,
                                                        javax.swing.GroupLayout.DEFAULT_SIZE,
                                                        javax.swing.GroupLayout.PREFERRED_SIZE))
                                .addContainerGap()));
    }// </editor-fold>
    //GEN-END:initComponents
    private void jButton1ActionPerformed(java.awt.event.ActionEvent evt) {
        testnumstr = totaltestnum.getText();
        totalnumstr = totalrunnum.getText();
        if (testnumstr.isEmpty() || totalnumstr.isEmpty()) {
        }
        double total = 0, a = Double.valueOf(totalnumstr);
        double b = Double.valueOf(testnumstr);
        int i = 0;
        for (i = 0; i < b; i++)
            total += getPi(a);
        total /= b;
        java.text.DecimalFormat df=new java.text.DecimalFormat("#.00000000");
        //控制输出格式
        resultstr = df.format(total);
        resultnum.setText(resultstr);
    }
    //GEN-BEGIN:variables
    // Variables declaration - do not modify
    private javax.swing.JPanel DrawPane;
    private javax.swing.JButton jButton1;
    private javax.swing.JLabel jLabel1;
    private javax.swing.JLabel jLabel2;
    private javax.swing.JLabel jLabel4;
    private javax.swing.JTextField resultnum;
    private javax.swing.JTextField totalrunnum;
    private javax.swing.JTextField totaltestnum;
    // End of variables declaration//GEN-END:variables
}