import java.util.Random;

public class ReadingRoomMonitor {
    private final int MAX_SEATS = 100;
    private final ReaderInfo[] seats = new ReaderInfo[MAX_SEATS];
    private int freeSeats = MAX_SEATS;

    public ReadingRoomMonitor() {
        for (int i = 0; i < MAX_SEATS; i++) {
            seats[i] = new ReaderInfo();
        }
    }

    public synchronized void enterRoom(String name) throws InterruptedException {
        while (freeSeats == 0) {
            System.out.println(name + " is waiting for a free seat.");
            wait();
        }

        for (int i = 0; i < MAX_SEATS; i++) {
            if (seats[i].isEmpty()) {
                seats[i].setName(name);
                seats[i].setSeatNumber(i + 1);
                System.out.println(name + " has taken seat " + (i + 1));
                break;
            }
        }

        freeSeats--;
        notifyAll();
    }

    public synchronized void leaveRoom(int seatNumber) {
        if (seatNumber > 0 && seatNumber <= MAX_SEATS && !seats[seatNumber - 1].isEmpty()) {
            System.out.println(seats[seatNumber - 1].getName() + " is leaving seat " + seatNumber);
            seats[seatNumber - 1].clear();
            freeSeats++;
            notifyAll();
        }
    }

    private class ReaderInfo {
        private int seatNumber;
        private String name;

        public boolean isEmpty() {
            return name == null || name.isEmpty();
        }

        public void setSeatNumber(int seatNumber) {
            this.seatNumber = seatNumber;
        }

        public void setName(String name) {
            this.name = name;
        }

        public String getName() {
            return name;  // 获取读者名字
        }

        public void clear() {
            this.seatNumber = 0;
            this.name = null;
        }
    }

    public static void main(String[] args) {
        ReadingRoomMonitor monitor = new ReadingRoomMonitor();
        Random random = new Random();
        final int NUM_THREADS = 2000;

        for (int i = 0; i < NUM_THREADS; i++) {
            new Thread(() -> {
                String threadName = Thread.currentThread().getName();
                try {
                    monitor.enterRoom(threadName);
                    // Simulate reading time
                    Thread.sleep(random.nextInt(1000));
                    int seatNumber = Integer.parseInt(threadName.substring(threadName.indexOf('-') + 1)) % 100 + 1;
                    monitor.leaveRoom(seatNumber);
                } catch (InterruptedException e) {
                    System.out.println(threadName + " was interrupted.");
                }
            }, "Reader-" + i).start();
        }
    }
}
