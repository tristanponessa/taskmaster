import os
import time
import shutil

class Collector:
    def __init__(self, runspath):
        """
        Collector constructor.
        Initializes the collection process by verifying the Avida directory and getting the task_quality files.
        :param: Where the collector should look for the tasks_quality files.
        """
        self.runs_path = runspath

        ### Dictionary indexed as path to run file => path to task_quality.dat
        self.task_qualities = self.collect_task_qualities()
        self.out_path = self.move_and_rename_files()

        if not self.task_qualities:
            return ## Nothing was found in the data_out directory.

    def collect_task_qualities(self):
        """
        Collects all the task quality files from the data_out directory in Avida.
        :return: list, collection of tasks_quality absolute file paths.
        """
        dirs = {}

        for dir in os.listdir(self.runs_path):
            dir = os.path.join(self.runs_path, dir)
            if os.path.isdir(dir):
                dirs[dir] = os.path.join(dir, "data/tasks_quality.dat")

        print str(len(dirs)) + " output directories have been found, now copying..."

        return dirs

    def move_and_rename_files(self):
        """
        We create e directory in the taskmaster/ directory called task_qualities_time().
        Currently, all of the tasks_quality.dat files have the same name, which is bad.
        So we'll rename them with the format *containing_folder*_tasks_quality.dat
        """
        dir = "task_qualities_" + time.strftime("%m_%d_%Y_%H_%M_%S") #$ This will contain all our tasks_quality files

        os.mkdir(dir)

        for key in self.task_qualities:
            ## This is a little lengthy and gross.
            ## It just copies and renames all the tasks_quality.dat files to the format described in the docstring.
            shutil.copy(self.task_qualities[key], "./" + dir + "/" + os.path.basename(key) + "_" + os.path.basename(self.task_qualities[key]))

        return dir

    def get_out_path(self):
        """
        Out path variable getter.
        Gets where the task quality files were output.
        :return: string
        """
        return self.out_path