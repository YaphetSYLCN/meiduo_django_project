// 创建Vue对象
let vm = new Vue(
    {
        el: '#app', // 通过ID选择器选定绑定HTML内容
        delimiters: ['[[', ']]'],
        data: { // 数据对象
            // v-model
            username: '',
            password: '',
            password2: '',
            mobile: '',
            allow: '',
            image_code_url: '',
            uuid: '',

            // v-show
            error_name: false,
            error_password: false,
            error_password2: false,
            error_mobile: false,
            error_allow: false,

            // error_message
            error_name_message: '',
            error_mobile_message: '',
        },
        mounted() { // 页面加载结束调用
            this.generate_image_code();
        },
        methods: { // 定义和实现事件方法
            // 生成图形验证码
            generate_image_code() {
                this.uuid = generateUUID();
                this.image_code_url = '/verify/image_codes/' + this.uuid;
            },

            // 校验用户名
            check_username() {
                let re = /^[a-zA-Z0-9_-]{5,20}$/;
                if (re.test(this.username)) {
                    this.error_name = false;
                } else {
                    this.error_name_message = '请输入5-20个字符的用户名';
                    this.error_name = true;
                }

                // 判断用户名是否重复注册
                if (this.error_name === false) {
                    let url = '/users/username/' + this.username + '/count/';
                    axios.get(url, {
                        responseType: "json",
                    })
                        .then(response => {
                            if (response.data.count === 1) {
                                // 用户已存在
                                this.error_name_message = "用户名已存在";
                                this.error_name = true;
                            } else {
                                this.error_name = false;
                            }
                        })
                        .catch(error => {
                            console.log(error.response);
                        })
                }
            },

            // 校验密码
            check_password() {
                let re = /^[0-9A-Za-z]{8,20}$/;
                this.error_password = !re.test(this.password);
            },

            // 校验确认密码
            check_password2() {
                this.error_password2 = this.password !== this.password2;
            },

            // 校验手机号码
            check_mobile() {
                let re = /^1[3-9]\d{9}$/;
                if (re.test(this.mobile)) {
                    this.error_mobile = false;
                } else {
                    this.error_mobile_message = "您输入的手机号格式不正确";
                    this.error_mobile = true;
                }
            },

            // 校验是否勾选协议
            check_allow() {
                this.error_allow = !this.allow;
            },

            // 监听表单提交事件
            on_submit() {
                this.check_username();
                this.check_password();
                this.check_password2();
                this.check_mobile();
                this.check_allow();

                // 禁用表单提交
                if (this.error_name === true || this.error_password === true || this.error_password2 === true ||
                    this.error_mobile === true || this.error_allow === true) {
                    window.event.returnValue = false;
                }
            },
        },
    }
)