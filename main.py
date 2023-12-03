class User:
    userlist = []
    id = 0

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password
        User.userlist.append(self)

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        try:
            if not all(x.isalpha() or x.isspace() for x in value):
                raise ValueError
        except ValueError:
            print("Name should only contain letters or spaces")
            while not all(x.isalpha() or x.isspace() for x in value):
                value = input("Re-enter your name:")
        self.__name = value

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, value):
        try:
            if "@" not in value or ".com" not in value:
                raise SyntaxError
        except SyntaxError:
            print("Enter proper email")
            value = input("Re-enter your email:")
        self.__email = value

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, value):
        self.__password = value

    @staticmethod
    def record_info():
        User.id += 1
        name = input("Enter your name: ")
        email = input("Enter your email: ")
        password = input("Enter your password: ")
        return name, email, password

    @staticmethod
    def login():
        uemail = input("Enter email: ")
        pword = input("Enter password: ")
        for i in User.userlist:
            if uemail != i.email:
                continue
            if pword != i.password:
                print("Password is incorrect")
                return None
            return i
        print("Email not found")
        return None


class Seeker(User):
    def __init__(self, name, email, password, description, skills):
        super().__init__(name, email, password)
        self.description = description
        self.skills = skills

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, value):
        self.__description = value

    @property
    def skills(self):
        return self.__skills

    @skills.setter
    def skills(self, value):
        self.__skills = value

    @staticmethod
    def record_info():
        name, email, password = User.record_info()
        skills = input("Enter your skills (Separate each skill by a comma): ")
        description = input("Enter a description for your profile: ")
        return Seeker(name, email, password, description, skills.replace(" ", "").lower().split(","))

    def recommended(self):
        recs = []
        count = 0
        for i in joblist:
            count = 0  # Reset count for each job
            for j in i.required_skills:
                if str(j).strip().lower() in self.skills:
                    count += 1
            if (count / len(i.required_skills)) > 0.6:
                recs.append(i)
        return recs

    def display_recs(self):
        recs = self.recommended()
        for i in recs:
            print(f"{' ' * 20}Title: {i.title}")
            print("Description: ", i.description)
            print("Required Skills: ", i.required_skills)
            print(f"Posted by {i.employer.name}")

        print("Select option:")
        print("1. Go back")
        print("2. Exit")
        print("OR Enter the id of the job you wish to apply to")
        x = input()
        if x == '1':
            return
        elif x == '2':
            exit()
        else:
            self.apply(x)

    def apply(self, job_id):
        for job in joblist:
            if str(job.id) == job_id:
                job.applicants.append(self)
                print(f"Successfully applied for the job: {job.title}")
                return
        print("Invalid job ID. Application failed.")


class Employer(User):
    def __init__(self, name, email, password, jobs):
        super().__init__(name, email, password)
        self.jobs = jobs
        self.applicants = []

    @staticmethod
    def record_info():
        name, email, password = User.record_info()
        return Employer(name, email, password, [])

    def post_job(self):
        name = input("Enter name of the job: ")
        skills = input("Enter required skills (separated by comma): ")
        description = input("Enter job description: ")
        job_obj = Job(self, name, skills.split(","), description)
        self.jobs.append(job_obj)
        joblist.append(job_obj)
        print(f"Job '{name}' successfully posted.")

    def see_applicants(self):
        if not self.jobs:
            print("No jobs posted yet.")
            return

        for job in self.jobs:
            print(f"Job Title: {job.title}")
            print("Applicants:")
            for applicant in job.applicants:
                print(f" - {applicant.name}")
            print()


class Job:
    num_of_instances = 0

    def __init__(self, employer, title, skills, description):
        Job.num_of_instances += 1
        self.employer = employer
        self.id = Job.num_of_instances
        self.title = title
        self.required_skills = skills
        self.description = description
        self.applicants = []


userlist = []
joblist = []

if __name__ == "__main__":
    while True:
        print("Welcome to JobJet")
        print("-" * 40)
        print("Select user type:")
        print("1. Job Seeker")
        print("2. Employer")
        print("3. Exit")
        choice = input()

        if choice == "1":
            obj = None
            choice2 = None
            while obj is None:
                print("Select option:")
                print("1. Log into account")
                print("2. Create a new account")
                print("3. Exit")
                choice2 = input()
                if choice2 == "1":
                    obj = User.login()
                elif choice2 == "2":
                    obj = Seeker.record_info()
                elif choice2 == "3":
                    break
                else:
                    print("Invalid choice")
                    continue

            if obj is not None:
                while True:
                    print("Select option:")
                    print("1. View recommended jobs")
                    print("2. Go back")
                    choice3 = input()
                    if choice3 == "1":
                        obj.display_recs()
                    elif choice3 == "2":
                        break
                    else:
                        print("Invalid choice")

        elif choice == "2":
            obj = None
            choice2 = None
            while obj is None:
                print("Select option:")
                print("1. Log into account")
                print("2. Create a new account")
                print("3. Exit")
                choice2 = input()
                if choice2 == "1":
                    obj = User.login()
                elif choice2 == "2":
                    obj = Employer.record_info()
                elif choice2 == "3":
                    break
                else:
                    print("Invalid choice")
                    continue

            if obj is not None:
                while True:
                    print("Select option:")
                    print("1. Post a job")
                    print("2. See applicants")
                    print("3. Go back")
                    choice3 = input()
                    if choice3 == "1":
                        obj.post_job()
                    elif choice3 == "2":
                        obj.see_applicants()
                    elif choice3 == "3":
                        break
                    else:
                        print("Invalid choice")

        elif choice == "3":
            break
        else:
            print("Invalid choice")
