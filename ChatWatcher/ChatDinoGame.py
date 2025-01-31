from BaseCode.TwitchChatMessageRunner import MessageRunner
from ChatListeners.DinoGameListener import DinoGameListener
from Games.DinoRunner import DinoRunner
import multiprocessing
import time

def start_dino_runner(action_options):
    dino_runner = DinoRunner(action_options)
    dino_runner.startRunner()

def main():
    with multiprocessing.Manager() as manager:
        action_options = manager.list()
        runner = MessageRunner()

        runner_process = multiprocessing.Process(target=runner.start, args=(0, [DinoGameListener(action_options)], 0.25))
        runner_process.start()

        dino_runner_process = multiprocessing.Process(target=start_dino_runner, args=(action_options,))
        dino_runner_process.start()

        try:
            while runner_process.is_alive():
                if not dino_runner_process.is_alive():
                    if "start" in action_options:
                        print("Starting new game...")
                        dino_runner_process = multiprocessing.Process(target=start_dino_runner, args=(action_options,))
                        dino_runner_process.start()
                        action_options[:] = []  # Clear the action options
                time.sleep(1)  # Sleep for a short time to avoid busy waiting
        except KeyboardInterrupt:
            print("Terminating processes...")
        finally:
            if runner_process.is_alive():
                runner_process.terminate()
            if dino_runner_process.is_alive():
                dino_runner_process.terminate()

if __name__ == "__main__":
    multiprocessing.set_start_method('spawn')  # Ensure 'spawn' method is used
    main()
