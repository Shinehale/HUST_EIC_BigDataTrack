# Chapter 6 并发程序设计

说明：C中只有线程，进程，C++21中引入协程，但都没有管程的概念，通用情况为conditional variable实现，所以选择了java作为算法实现的语言，其中`synchronized` 关键字可以让这个函数作为原子操作来完成

## 应用题

### T17

#### version 1 信号量和PV操作

考虑使用两个信号量对问题进行描述：

- `mutex(初值: 1)` 确保对登记表的互斥访问（本质上是个锁）
- `emptySeats(初值：100)` 保证对座位的控制权的访问

读者进入：(1) `P(emptySeats)` (2) 锁定登记表 `P(mutex)`，记录表中的信息(`insert`)，可以是map数据结构 解锁登记表`V(mutex)`

读者离开: (1) 锁定登记表`P(mutex)`，从表中删除信息(`delete`)，然后解锁`V(mutex)`  (2) `V(emptySeats)`

#### version2: 使用管程

```java
public synchronized void enterRoom(String name) throws InterruptedException {
        // 等待直到有空座位
        while (freeSeats == 0) {
            wait();
        }

        // 寻找一个空闲座位并登记
        for (int i = 0; i < MAX_SEATS; i++) {
            if (seats[i].isEmpty()) {
                seats[i].setName(name);
                seats[i].setSeatNumber(i + 1);  // 座位号从1开始计数
                break;
            }
        }

        freeSeats--;
        notifyAll();  // 通知其他可能等待的线程
    }

    public synchronized void leaveRoom(int seatNumber) {
        // 注销座位
        if (seatNumber > 0 && seatNumber <= MAX_SEATS && !seats[seatNumber - 1].isEmpty()) {
            seats[seatNumber - 1].clear();  // 清空座位信息
            freeSeats++;
            notifyAll();  // 通知等待进入的线程
        }
    }
```

#### T18

#### version 1 信号量和PV操作

定义如下的信号量来实现:

- `mutex(1)` 保证对盘子状态的互斥访问
- `apples(0)` 盘中苹果的数量
- `oranges(0)`盘中橘子的数量
- `emptySlots(2)` 盘中空槽的数量

父亲放入苹果: (1) `P(emptySlots)` 确保有空槽否则等待 (2) `P(mutex)` 获取对盘子状态访问权,  `V(apples)` 增加苹果的数量 `V(mutex)` 释放盘子控制权

母亲放入橘子: (1) `P(emptySlots)` 确保有空槽否则等待 (2) `P(mutex)` 获取对盘子状态访问权,  `V(oranges)` 增加苹果的数量 `V(mutex)` 释放盘子控制权

儿子吃橘子: (1) `P(orangles)`确保盘子中有橘子 (2) `P(mutex)` 获取对盘子状态访问权,  `V(emptySlots)` 增加空盘的数量 `V(mutex)` 释放盘子控制权

女儿吃苹果: (1) `P(apples)`确保盘子中有苹果 (2) `P(mutex)` 获取对盘子状态访问权,  `V(emptySlots)` 增加空盘的数量 `V(mutex)` 释放盘子控制权

#### version2: 使用管程

```java
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
```

#### T25

当 $m>n$ 时， 假设一个进程最多可以请求$x$个资源，故当
$$
m > n * (x -1)
$$
时，不会发生死锁，化简得到
$$
x <\frac{m}{n} + 1
$$
当$m$是$n$的倍数时,$x=\frac{m}{n}$，否则为$x=\lfloor \frac{m}{n} \rfloor + 1 $

现在考虑$m \le n$的情况，此时最多每个进程最多可以请求$1$个资源

#### T30

考虑如下的情况，$P_1$ 申请到了$R_1$ 并且申请到了 $R_2$, 现在将要额外申请$R_1$,此时$P_2, P_3$也进行到了这个状态，而$P_4$ 将要申请$R_1$的资源，但是$R_1$的资源只有三个，无法满足，只好等待，查看此时的资源分配表

| process | R1_require | R1_allocated |
| ------- | ---------- | ------------ |
| P1      | 2          | 1            |
| P2      | 2          | 1            |
| P3      | 2          | 1            |
| P4      | 2          | 0            |

此时$P_1, P_2, P_3$进程都将等待新的$R_1$但是他们都不释放自己已有的$R_1$资源，即产生了明显的循环等待，最终造成了死锁