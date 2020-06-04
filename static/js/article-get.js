var vm = new Vue({
    // v-cloak 指令是解决屏幕闪动的好方法
    el: '#atd',
    // 修改Vue变量的读取语法，避免和django模板语法冲突
    delimiters: ['[[', ']]'],
    data: {
        article_data: [],
    },
    mounted() {
        // 获取文章
        this.get_article_data();
    },
    methods: {
        // 获取文章数据
        get_article_data() {
            let url = location.origin + '/article_detail/';
            // console.log(location.origin);
            axios.get(url, {
                responseType: 'json'
            })
                //请求成功处理 =>箭头函数 相当于return花括号里的内容
                .then(response => {
                    window.article_data = response.data.article_list;
                    // console.log(response.data.article_list);
                    // console.log(this.article_data, 'cesi');
                })
                // 请求失败处理
                .catch(error => {
                    console.log(error.response);
                })
        },
    }
});
