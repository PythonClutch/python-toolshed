from .extensions import db, bcrypt, login_manager
from marshmallow import Schema, fields, ValidationError
from flask.ext.login import UserMixin
import arrow


@login_manager.user_loader
def load_admin(admin_id):
    return AdminAccount.query.get(admin_id)


"""
Models
"""


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    github_name = db.Column(db.String(255), nullable=False)
    github_url = db.Column(db.String(400))
    email = db.Column(db.String(255))
    avatar_url = db.Column(db.String(255))

    comments = db.relationship("Comment", backref="user", lazy="dynamic", foreign_keys="Comment.user_id",
                               cascade="all,delete")
    like = db.relationship("Like", backref="user", lazy="dynamic", foreign_keys="Like.user_id",
                           cascade="all,delete")

    submissions = db.relationship("Project", backref="submitted_by",
                                   lazy="dynamic", cascade="all,delete",
                                   foreign_keys="Project.submitted_by_id")

    def __repr__(self):
        return "User: {}".format(self.github_name)


class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))

    @property
    def user_name(self):
        return self.user.github_name

    @property
    def project_name(self):
        return self.project.name

    def __repr__(self):
        return "{} likes {}".format(self.user.github_name, self.project.name)


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    status = db.Column(db.Boolean)
    name = db.Column(db.String(255), nullable=False, unique=True)
    summary = db.Column(db.String(400))
    forks_count = db.Column(db.Integer)
    starred_count = db.Column(db.Integer)
    watchers_count = db.Column(db.Integer)
    watchers_url = db.Column(db.String)
    current_version = db.Column(db.String(20))
    last_commit = db.Column(db.DateTime)
    first_commit = db.Column(db.DateTime)
    open_issues_count = db.Column(db.Integer)
    project_stub = db.Column(db.String(400))
    downloads_count = db.Column(db.Integer)
    contributors_count = db.Column(db.Integer)
    python_three_compatible = db.Column(db.Boolean)
    date_added = db.Column(db.Date)
    score = db.Column(db.Float)
    website = db.Column(db.String(400))
    git_url = db.Column(db.String(400))
    pypi_url = db.Column(db.String(400))
    contributors_url = db.Column(db.String(400))
    mailing_list_url = db.Column(db.String(400))
    forks_url = db.Column(db.String(400))
    starred_url = db.Column(db.String)
    open_issues_url = db.Column(db.String(400))
    docs_url = db.Column(db.String(400))

    submitted_by_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    group_id = db.Column(db.Integer, db.ForeignKey("group.id"))
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))

    comments = db.relationship("Comment", backref="project", lazy="dynamic", foreign_keys="Comment.project_id",
                               cascade="all,delete")
    user_likes = db.relationship("Like", backref="project", lazy="dynamic", foreign_keys="Like.project_id",
                                 cascade="all,delete")
    logs = db.relationship("ProjectLog", backref="project", lazy="dynamic", foreign_keys="ProjectLog.project_id",
                           cascade="all,delete")

    @property
    def number_of_comments(self):
        return len(Comment.query.filter_by(project_id=self.id).all())

    @property
    def number_of_likes(self):
        return len(Like.query.filter_by(project_id=self.id).all())

    @property
    def age_display(self):
        if not self.first_commit:
            return None
        else:
            age_string = str(self.first_commit)
            arrow_age = arrow.get(age_string)
            return arrow_age.humanize()

    @property
    def first_commit_display(self):
        if not self.first_commit:
            return None
        else:
            first_string = str(self.first_commit)
            arrow_first_commit = arrow.get(first_string)
            return arrow_first_commit.humanize()

    @property
    def last_commit_display(self):
        if not self.last_commit:
            return None
        else:
            last_string = str(self.last_commit)
            arrow_last_commit = arrow.get(last_string)
            return arrow_last_commit.humanize()


    def __repr__(self):
        return "{}".format(self.name)


class ProjectLog(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    forks_count = db.Column(db.Integer)
    starred_count = db.Column(db.Integer)
    watchers_count = db.Column(db.Integer)
    current_version = db.Column(db.String(20))
    last_commit = db.Column(db.DateTime)
    open_issues_count = db.Column(db.Integer)
    downloads_count = db.Column(db.Integer)
    contributors_count = db.Column(db.Integer)
    log_date = db.Column(db.Date)
    likes_count = db.Column(db.Integer)
    previous_score = db.Column(db.Float)

    project_id = db.Column(db.Integer, db.ForeignKey("project.id"))

    @property
    def stars_difference(self):
        return Project.query.get(self.project_id) - self.starred_count

    @property
    def forks_difference(self):
        return Project.query.get(self.project_id) - self.forks_count

    @property
    def watchers_difference(self):
        return Project.query.get(self.project_id) - self.watchers_count

    @property
    def download_difference(self):
        return Project.query.get(self.project_id) - self.downloads_count

    @property
    def contributor_difference(self):
        return Project.query.get(self.project_id) - self.contributors_count

    @property
    def likes_difference(self):
        return Project.query.get(self.project_id) - self.contributors_count


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.String(400))
    created = db.Column(db.DateTime)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"))

    def __repr__(self):
        return "Comment: {}".format(self.text)


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))

    projects = db.relationship("Project", backref="group", lazy="dynamic", foreign_keys="Project.group_id")
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))

    def __repr__(self):
        return "Group: {}".format(self.name)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))

    projects = db.relationship("Project", backref="category", lazy="dynamic", foreign_keys="Project.category_id")
    groups = db.relationship("Group", backref="category", lazy="dynamic", foreign_keys="Group.category_id")

    def __repr__(self):
        return "Category: {}".format(self.name)


class AdminAccount(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    admin_name = db.Column(db.String(255), nullable=False)
    encrypted_password = db.Column(db.String(60))

    def get_password(self):
        return getattr(self, "_password", None)

    def set_password(self, password):
        self._password = password
        self.encrypted_password = bcrypt.generate_password_hash(password)

    password = property(get_password, set_password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.encrypted_password, password)

    def __repr__(self):
        return "Admin {}".format(self.admin_name)


"""
Schemas

For schemas we need to figure out how to make them more restful by adding
the ability to display the api endpoints.
"""


class CommentSchema(Schema):
    class Meta:
        fields = ("id", "text", "created", "user_id",
                  "project_id")


class UserSchema(Schema):
    comments = fields.Nested(CommentSchema, many=True)

    class Meta:
        fields = ("id", "github_name", "github_url", "email", "comments")


class LikeSchema(Schema):
    class Meta:
        fields = ("id", "user_id", "project_id", "user_name", "project_name")


class LogSchema(Schema):
    class Meta:
        fields = ("id", "project_id", "forks_count", "starred_count",
                  "current_version", "last_commit", "open_issues_count",
                  "downloads_count", "contributors_count", "log_date",
                  "stars_difference", "forks_difference", "watchers_difference",
                  "download_difference", "contributor_difference", "likes_difference")


class ProjectSchema(Schema):
    comments = fields.Nested(CommentSchema, many=True)
    user_likes = fields.Nested(LikeSchema, many=True)
    logs = fields.Nested(LogSchema, many=True)

    class Meta:
        fields = ("id", "status", "name", "summary", "forks_count",
                  "starred_count", "watchers_count", "watchers_url",
                  "current_version", "last_commit", "first_commit",
                  "open_issues_count", "project_stub", "downloads_count",
                  "contributors_count", "python_three_compatible", "website",
                  "git_url", "pypi_url", "contributors_url", "mailing_list_url",
                  "forks_url", "starred_url", "open_issues_url", "docs_url",
                  "group_id", "category_id", "comments", "user_likes", "age_display",
                  "last_commit_display", "logs", "date_added", "first_commit_display")


class GroupSchema(Schema):
    projects = fields.Nested(ProjectSchema, many=True)

    class Meta:
        fields = ("id", "name", "projects", "category_id")


class CategorySchema(Schema):
    groups = fields.Nested(GroupSchema, many=True)

    class Meta:
        fields = ("id", "name", "groups")
