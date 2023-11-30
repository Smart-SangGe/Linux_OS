#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>

int main()
{
    pid_t pid;

    // 创建子进程
    pid = fork();

    if (pid < 0)
    {
        // fork 失败
        fprintf(stderr, "Fork failed");
        return 1;
    }
    else if (pid == 0)
    {
        // 子进程
        printf("This is the child process. PID = %d\n", getpid());
    }
    else
    {
        // 父进程
        printf("This is the parent process. PID = %d, Child PID = %d\n", getpid(), pid);
    }

    return 0;
}
