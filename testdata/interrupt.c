#include "init.h"
#include "encoding.h"

static volatile unsigned interrupt_count;
static volatile unsigned local;
static volatile unsigned ghartid;

static unsigned delta = 10;
void *interrupt_hander(unsigned hartid, unsigned mcause, void *mepc, void *sp)
{
    interrupt_count++;
    ghartid = hartid;
    // MTIMECMP[0] = MTIME + delta;
    return mepc;
}

int fact (int N) {
    if (N <= 1) {
        return 1;
    }else{
        return N*fact(N-1);
    }
}

/*
int main()
{
    interrupt_count = 0;
    local = 0;

    set_trap_handler(hander);
    // MTIMECMP[0] = MTIME + 10;
    enable_timer_interrupts();

    while (1) {
        local++;
    }
}
*/
