public class FruitBowl {
    private int apples = 0;
    private int oranges = 0;
    private final int capacity = 2;

    // 放入苹果
    public synchronized void putApple() throws InterruptedException {
        while (apples + oranges >= capacity) {
            wait(); // 等待有空槽
        }
        apples++;
        notifyAll(); // 唤醒可能在等待苹果的线程
    }

    // 放入橘子
    public synchronized void putOrange() throws InterruptedException {
        while (apples + oranges >= capacity) {
            wait(); // 等待有空槽
        }
        oranges++;
        notifyAll(); // 唤醒可能在等待橘子的线程
    }

    // 吃苹果
    public synchronized void takeApple() throws InterruptedException {
        while (apples == 0) {
            wait(); // 等待有苹果
        }
        apples--;
        notifyAll(); // 唤醒可能在等放入水果的线程
    }

    // 吃橘子
    public synchronized void takeOrange() throws InterruptedException {
        while (oranges == 0) {
            wait(); // 等待有橘子
        }
        oranges--;
        notifyAll(); // 唤醒可能在等放入水果的线程
    }
}
