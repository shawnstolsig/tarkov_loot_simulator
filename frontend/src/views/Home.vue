<template>
	<v-container>
		<v-card>
			<v-card-title>
				Home page (testing)
			</v-card-title>
			<v-card-text>
				<v-btn @click="showItem">
					Test Tarkov Market API
				</v-btn>
			</v-card-text>
			<v-card-actions>
				<v-text-field
					label="Input"
					v-model="inputString"
				></v-text-field>
				<v-text-field
					v-model="shortName"
					outlined
					readonly
					label="Short Name"
				></v-text-field>
				<v-text-field
					v-model="price"
					outlined
					readonly
					label="24hr Avg Price"
				></v-text-field>
				<v-img :src="image"></v-img>
			</v-card-actions>
		</v-card>
	</v-container>
</template>

<script>
import axios from 'axios'

export default {
	name: 'Home',
	components: {
		
	},
	data(){
		return {
			inputString: null,
			shortName: '(blank)',
			price: '(blank)',
			image: '',
		}
	},  // end data
	methods: {

		// get item info from Tarkov Market API
		showItem(){
			console.log(`Pulling Tarkov Market for ${this.inputString}`)
			axios({
				method: 'get',
				url: `https://tarkov-market.com/api/v1/item`,
				params: {
					q: this.inputString,
				},
				headers: {'x-api-key': 'm07rRZrjmjRMHtsP'},
				
			})
			.then(response => {
				console.log(response)
				if(response.data.length > 0 ){
					this.shortName = response.data[0].shortName
					this.price = response.data[0].avg24hPrice
					this.image = response.data[0].icon
				}
			})
			.catch(error => {console.log(error)})
		}
	},  // end methods
	computed: {
	
	}   // end computed   

}
</script>
