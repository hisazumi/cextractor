#include "init.h"
#include "encoding.h"

static volatile unsigned interrupt_count;
static volatile unsigned local;
static volatile unsigned ghartid;

static unsigned delta = 10;
void *hander(unsigned hartid, unsigned mcause, void *mepc, void *sp)
{
    interrupt_count++;
    ghartid = hartid;
    // MTIMECMP[0] = MTIME + delta;
    return mepc;
}

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
