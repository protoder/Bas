'use strict';

var root = {
	data() 
	{
		return {

		}
	},//data
	
	computed: {
		
		
	},//computed
	
	methods: {
		
		
	},//methods
		
	mounted() {
		
	},//mounted
	
	components: {
		'top':   header,
		'content':  content,
		'foot':   footer,
	},//components
}//root

const app = Vue.createApp(root);
const vm = app.mount('#app');