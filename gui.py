from tkinter import *
from tkinter import filedialog


class ProjectManager:
    def __init__(self):
        self.window = Tk()
        self.window.title("Project Manager")

        self.path_dir = None

        # Set Project Name
        self.proj = Label(text="Project Name: ")
        self.proj.grid(row=0, column=0)

        self.proj_name = Entry()
        self.proj_name.grid(row=0, column=1)

        # Create Path Button
        self.path_btn = Button(text="Set Path...", command=self.set_path)
        self.path_btn.grid(row=1, column=0)

        # Create Path Label
        self.path_label = Label(padx=100, bg="white", fg="black")
        self.path_label.grid(row=1, column=1)

        # Create Subfolders
        frame = LabelFrame(text="Select the Subjects", padx=20, pady=20)
        frame.grid(row=2, column=0)
        subfolders = {"geo", "hip", "renders", "textures", "flipbook"}
        self.vars = []
        for i, folder in enumerate(subfolders):
            var = StringVar()
            cb = Checkbutton(
                frame,
                text=folder,
                variable=var,
                onvalue=folder,
                offvalue="",
                fg="black",
            ).pack(side=TOP, anchor=W)
            self.vars.append(var)

        Button(frame, text="Create!", command=self.create).pack()

        self.window.mainloop()

    def create(self):
        # extract roll numbers for checked checkbuttons
        dirs = [var.get() for var in self.vars if var.get()]
        proj_dir = self.path_dir + "/" + self.proj_name.get()
        os.mkdir(proj_dir)
        for dir in dirs:
            os.mkdir(proj_dir + "/" + dir)

    def set_path(self):
        self.path_dir = filedialog.askdirectory()
        self.path_label.config(text=self.path_dir)


if __name__ == "__main__":
    ui = ProjectManager()
