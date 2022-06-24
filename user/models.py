from django.db import models

# Create your models here.
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
# custom user model 사용 시 UserManager 클래스와 create_user, create_superuser 함수가 정의되어 있어야 함

class UserManager(BaseUserManager): # 커스텀 User를 쓰려면 무조건 정의 해줘야함
    def create_user(self, username, password=None):
        if not username:
            raise ValueError('Users must have an username')
        user = self.model(
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

          # python manage.py createsuperuser 사용 시 해당 함수가 사용됨
    def create_superuser(self, username, password):
        user = self.create_user(
            username=username,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
class User(AbstractBaseUser):

    GENDERS = (
        ('M', '남성(Man)'), ('W', '여성(Woman)'),
    )

    username = models.CharField("사용자 계정", max_length=20, unique=True)
    email = models.EmailField("이메일 주소", max_length=100)
    phone_number = models.CharField("전화번호", max_length=30, unique=True)
    password = models.CharField("비밀번호", max_length=128)
    fullname = models.CharField("이름", max_length=20)
    join_date = models.DateTimeField("가입일", auto_now_add=True)
    gender = models.CharField(verbose_name='성별', max_length=1, choices=GENDERS, default='')


		# is_active가 False일 경우 계정이 비활성화됨
    is_active = models.BooleanField(default=True) 

    # is_seller가 False일 경우 구매자 계정으로 전환됨
    is_seller = models.BooleanField(default=False) 

    # is_staff에서 해당 값 사용
    is_admin = models.BooleanField(default=False)
    
    # id로 사용 할 필드 지정.
    # 로그인 시 USERNAME_FIELD에 설정 된 필드와 password가 사용된다.
    USERNAME_FIELD = "username" # email로 로그인하게 설정

    # user를 생성할 때 입력받은 필드 지정
    REQUIRED_FIELDS = [] # ["email", "gender"]
    
    objects = UserManager() # custom user 생성 시 필요
    
    def __str__(self):
        return self.username # f"{self.username} / {self.email}"

    # 로그인 사용자의 특정 테이블의 crud 권한을 설정, perm table의 crud 권한이 들어간다.
    # admin일 경우 항상 True, 비활성 사용자(is_active=False)의 경우 항상 False
    def has_perm(self, perm, obj=None):
        return True
    
    # 로그인 사용자의 특정 app에 접근 가능 여부를 설정, app_label에는 app 이름이 들어간다.
    # admin일 경우 항상 True, 비활성 사용자(is_active=False)의 경우 항상 False
    def has_module_perms(self, app_label): 
        return True
    
    # admin 권한 설정
    @property
    def is_staff(self): 
        return self.is_admin

    # 사용자계정으로 email을 사용, 추후 넷플릭스처럼 이메일 or 핸드폰 로그인 추가예정
    # objects = UserManager() 
    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = []

class UserProfile(models.Model):
    user = models.OneToOneField(to=User, verbose_name="사용자", on_delete=models.CASCADE, primary_key=True)
    interests = models.ManyToManyField(to="Interest", verbose_name="흥미")
    introduction = models.TextField("소개")
    birthday = models.DateField("생일")
    age = models.IntegerField("나이")

    def __str__(self) -> str:
        return f"{self.user.fullname}님의 프로필입니다."

class Interest(models.Model):
    name = models.CharField("흥미", max_length=50)
    def __str__(self):
        return self.name











# class UserSeller(AbstractBaseUser):

#     GENDERS = (
#         ('M', '남성(Man)'), ('W', '여성(Woman)'),
#     )

#     username = models.CharField("판매자 계정", max_length=20, unique=True)
#     email = models.EmailField("이메일 주소", max_length=100)
#     phone_number = models.CharField("전화번호", max_length=30, unique=True) 
#     # # 슈퍼유저를 폰넘버 만들기 전에 만들어서 makemigrations가 안 됨. 나중에 추가할 때 user 삭제 후 사용하기
#     password = models.CharField("비밀번호", max_length=128)
#     fullname = models.CharField("이름", max_length=20)
#     join_date = models.DateTimeField("가입일", auto_now_add=True)
#     gender = models.CharField(verbose_name='성별', max_length=1, choices=GENDERS, default='')
#     business_registration = models.CharField("사업자등록번호", max_length=10, unique=True)



# 	# is_active가 False일 경우 계정이 비활성화됨
#     is_active = models.BooleanField(default=True) 

#     # is_seller가 False일 경우 구매자 계정으로 전환됨
#     is_seller = models.BooleanField(default=True) 

#     # is_staff에서 해당 값 사용
#     is_admin = models.BooleanField(default=False)
    
#     # id로 사용 할 필드 지정.
#     # 로그인 시 USERNAME_FIELD에 설정 된 필드와 password가 사용된다.
#     USERNAME_FIELD = "username" # email로 로그인하게 설정

#     # user를 생성할 때 입력받은 필드 지정
#     REQUIRED_FIELDS = [] # ["email", "gender"]
    
#     objects = UserManager() # custom user 생성 시 필요
    
#     def __str__(self):
#         return self.username # f"{self.username} / {self.email}"

#     # 로그인 사용자의 특정 테이블의 crud 권한을 설정, perm table의 crud 권한이 들어간다.
#     # admin일 경우 항상 True, 비활성 사용자(is_active=False)의 경우 항상 False
#     def has_perm(self, perm, obj=None):
#         return True
    
#     # 로그인 사용자의 특정 app에 접근 가능 여부를 설정, app_label에는 app 이름이 들어간다.
#     # admin일 경우 항상 True, 비활성 사용자(is_active=False)의 경우 항상 False
#     def has_module_perms(self, app_label): 
#         return True
    
#     # admin 권한 설정
#     @property
#     def is_staff(self): 
#         return self.is_admin

#     # 사용자계정으로 email을 사용, 추후 넷플릭스처럼 이메일 or 핸드폰 로그인 추가예정
#     # objects = UserManager() 
#     # USERNAME_FIELD = 'email'
#     # REQUIRED_FIELDS = []


# class UserSellerProfile(models.Model):
#     user = models.OneToOneField(to=UserSeller, verbose_name="판매자", on_delete=models.CASCADE, primary_key=True)
#     interests = models.ManyToManyField(to="Interest", verbose_name="흥미")
#     introduction = models.TextField("소개")
#     birthday = models.DateField("생일")
#     age = models.IntegerField("나이")

#     def __str__(self) -> str:
#         return f"{self.user.fullname}님의 프로필입니다."