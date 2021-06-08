# KY_django

## 웹서비스

### Front-End

웹브라우저에서 특정 주소를 가진 서버 컴퓨터에 요청을 보내면 서버에서 제공하는 웹사이트가 제공됩니다. (ex. html파일을 받아 렌더링해서 화면에 보여줍니다.)

예를들어, a 태그를 가진 영역을 클릭하면 웹 브라우저는 다시 해당 주소를 가진 서버에 html 파일을 요청하고, 서버에서 받아 렌더링해서 보여줍니다.

이처럼 보여주는 화면이 Front-End입니다. 여기에 사용되는 프로그래밍 언어는 다양합니다.

- html
- css
- js

디자인을 편리하게 만들어주는 Api와 같은 [Bootstrap V5.0](https://getbootstrap.com/docs/5.0/getting-started/introduction/)을 CDN방식으로 사용하여 디자인하였습니다.

> CDN : Contents delivery network
> 
> Bootstrap 처럼 웹사이트에서 코드를 바로 가져오는 방식

### Back-End

웹사이트를 이용하는 방문자의 행동을 저장하고 보여주기 위해서는 행동에 반응하여 Front-End에 변화를 줄 수 있는 Back-End가 필요합니다.

웹사이트에 필요한 공통적인 필수기능이 있습니다. (CRUD)
- Create 생성
- Read 조회
- Update 수정
- Delete 삭제

+alpha : 웹사이트 관리자 페이지

웹프레임워크는 이와 같은 작업을 더 쉽게 개발할 수 있도록 도와줍니다.
> 웹프레임워크 : 웹 사이트 구현에 사용되는 복잡한 기능을 쉽게 만들 수 있도록 도와주는 도구모음집

Back-End를 Django로 구현하였습니다.

- Java는 JSP, spring
- 자바스크립트는 node.js
- 파이썬은 Django

#### 특징

- 프로젝트 생성과 동시에 관리자 페이지가 생성됨. 관리자 페이지에서 현재 웹사이트의 DB 구조를 파악할 수 있으며 수정/삭제도 가능하다.
- Django의 보안 가아디으 따라 웹 개발을 진행하여 보안 실수를 방지할 수 있음.



## Pages 

1. [Door Page](#Door-Page)
2. [Post List](#Post-List)
3. [Post Detail](#Post-Detail)
4. [Log in](#Log-in)
5. [About Me](#About-Me)

### Door Page

![Door Page](start.png)

---

### Post List

![Post List](post_list.png)

![post_list_footer](post_list_footer.png)

---

### Post Detail

![post_detail](post_detail.png)

---

### Log in

![Log in](login.png)

---

### About Me

![About Me](aboutme.png)
