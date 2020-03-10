<template>
	<v-container>
		<!-- Game settings -->
		<v-card>
			<v-row>
				<v-spacer></v-spacer>
				<v-col cols="4" md="4">
					<v-text-field
						label="Number of items"
						v-model="itemCount"
						type="number"
						min='1'
						max="12"
					></v-text-field>
				</v-col>

				<v-col cols="2" md="4">
					<v-btn @click="generateItems" class="fill-width">
						Generate
					</v-btn>
				</v-col>
				<v-spacer></v-spacer>
			</v-row>
		</v-card>

		<!-- Generated  -->
		<v-row >
			<v-spacer></v-spacer>
			<!-- Right side: unselected items -->
			<v-col cols="6">

				<!-- The available items inventory -->
				<v-tooltip bottom open-delay='500' v-for="i in selectedItems.length" :key="i">
					<template v-slot:activator="{ on }">
						<img :src="selectedItems[i-1].image_url" v-on="on" @click="moveToUnselected(i-1)"/>
					</template>
					<span>{{ selectedItems[i-1].long_name }}</span>
				</v-tooltip>	

			</v-col>
			
			<v-spacer></v-spacer>
			<!-- Left side: selected items -->
			<v-col cols="6">

				<v-tooltip bottom open-delay='500' v-for="i in unselectedItems.length" :key="i">
					<template v-slot:activator="{ on }">
						<img :src="unselectedItems[i-1].image_url" v-on="on" @click="moveToSelected(i-1)"/>
					</template>
					<span>{{ unselectedItems[i-1].long_name }}</span>
				</v-tooltip>	

			</v-col>

			<v-spacer></v-spacer>
		</v-row>
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
			// dimensions for game
			itemCount: 6,

			// data for game
			allItems: [],
			unselectedItems: [],
			selectedItems: []
		}
	},  // end data
	methods: {

		// Generate random items
		generateItems(){
			// reset game data
			this.unselectedItems = [];
			this.selectedItems = [];

			// loop through req'd num of items
			for(let i = 0; i < parseInt(this.itemCount); i++){

				// push an item at random from allItems
				let item = this.allItems[Math.floor(Math.random()*this.allItems.length)]
				this.unselectedItems.push(item)
			}
		},

		// Move from unselected to selected
		moveToSelected(i){
			this.selectedItems.push(this.unselectedItems[i]);
			this.unselectedItems.splice(i,1);
		},

		// Move from selected to unselected
		moveToUnselected(i){
			this.unselectedItems.push(this.selectedItems[i]);
			this.selectedItems.splice(i,1);
		},

	},  // end methods
	computed: {
		
	},   // end computed   
	mounted(){
		// when page is mounted, retrieve all item info from backend
		axios({
			method: 'get',
			url: `${this.$store.getters.backendEndpoints.api}/items/`,
		})
		.then(response => {
			console.log(response)
			this.allItems = response.data
			// initialize game when page loads
			this.generateItems()
		})
		.catch(error => {console.log(error)})


	},   // end mounted

}
</script>
