var vm = new Vue({
    // v-cloak 指令是解决屏幕闪动的好方法
    //new_article
    el: '#nat',
    // 修改Vue变量的读取语法，避免和django模板语法冲突
    delimiters: ['[[', ']]'],
    data: {
        article_data: [],
        category_data: [],
        tags_data: []
    },
    mounted() {
        // 获取最新文章数据 分类数据 标签数据
        this.get_data();

        // 获取标签数据
        this.get_tag();
        // this.get_category();
        this.get_cate();
    },
    methods: {
        // 获取数据
        get_data() {
            let url = location.origin + '/articles/GetNewArticle/';
            console.log(location.origin);
            axios.get(url, {
                responseType: 'json'
            })
                //请求成功处理 =>箭头函数 相当于return花括号里的内容
                .then(response => {
                    this.article_data = response.data.article_list;
                })
                // 请求失败处理
                .catch(error => {
                    console.log(error.response);
                })
        },
        get_tag() {
            let url = location.origin + '/articles/GetTags/';
            console.log(location.origin);
            axios.get(url, {
                responseType: 'json'
            })
                //请求成功处理 =>箭头函数 相当于return花括号里的内容
                .then(response => {
                    this.tags_data = response.data.tags_list;
                })
                // 请求失败处理
                .catch(error => {
                    console.log(error.response);
                })
        },
        get_cate() {
            let url = location.origin + '/articles/GetCateGory/';
            console.log(location.origin);
            axios.get(url, {
                responseType: 'json'
            })
                //请求成功处理 =>箭头函数 相当于return花括号里的内容
                .then(response => {
                    this.category_data = response.data.category_list;
                })
                // 请求失败处理
                .catch(error => {
                    console.log(error.response);
                })
        },
    }
});
