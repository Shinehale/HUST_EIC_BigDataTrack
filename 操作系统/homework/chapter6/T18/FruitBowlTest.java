public class FruitBowlTest {
    public static void main(String[] args) {
        final FruitBowl bowl = new FruitBowl();
        final int NUM_ACTIONS = 10; // 每种动作执行的次数

        // 爸爸线程，放苹果
        Thread dad = new Thread(() -> {
            for (int i = 0; i < NUM_ACTIONS; i++) {
                try {
                    bowl.putApple();
                    System.out.println("Dad placed an apple.");
                    Thread.sleep(100); // 稍作延迟模拟现实操作
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        });

        // 妈妈线程，放橘子
        Thread mom = new Thread(() -> {
            for (int i = 0; i < NUM_ACTIONS; i++) {
                try {
                    bowl.putOrange();
                    System.out.println("Mom placed an orange.");
                    Thread.sleep(100);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        });

        // 儿子线程，吃橘子
        Thread son = new Thread(() -> {
            for (int i = 0; i < NUM_ACTIONS; i++) {
                try {
                    bowl.takeOrange();
                    System.out.println("Son ate an orange.");
                    Thread.sleep(150);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        });

        // 女儿线程，吃苹果
        Thread daughter = new Thread(() -> {
            for (int i = 0; i < NUM_ACTIONS; i++) {
                try {
                    bowl.takeApple();
                    System.out.println("Daughter ate an apple.");
                    Thread.sleep(150);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        });

        // 启动所有线程
        dad.start();
        mom.start();
        son.start();
        daughter.start();

        // 等待所有线程完成
        try {
            dad.join();
            mom.join();
            son.join();
            daughter.join();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        System.out.println("All actions completed.");
    }
}
