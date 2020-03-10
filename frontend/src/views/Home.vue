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
						min='2'
						max='300'
					></v-text-field>
				</v-col>
				<v-col cols="4" md="4">
					<v-text-field
						label="Number of choices"
						v-model="pickLimit"
						type="number"
						min='1'
						:max="itemCount"
					></v-text-field>
				</v-col>

				<v-col cols="2" md="2">
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

		<!-- Submit button -->
		<v-row>
			<v-spacer></v-spacer>
			<v-col cols="1">
				<v-btn @click="submitChoices">
					Submit
				</v-btn>
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
			// game settings
			itemCount: 6,
			pickLimit: 1,
			pickCounter: 0,

			// game data
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
			this.pickCounter = 0;

			// loop through req'd num of items
			for(let i = 0; i < parseInt(this.itemCount); i++){

				// push an item at random from allItems
				let item = this.allItems[Math.floor(Math.random()*this.allItems.length)]
				this.unselectedItems.push(item)
			}
		},

		// Move from unselected to selected
		moveToSelected(i){
			// check to see if limit reached
			if(this.picksRemaining == 0){
				// do nothing
				alert("No picks remaining")
				
			} else {
				// push onto selected, remove from unselected
				this.selectedItems.push(this.unselectedItems[i]);
				this.unselectedItems.splice(i,1);

				// increment pick counter
				this.pickCounter++;
			}

		},

		// Move from selected to unselected
		moveToUnselected(i){
			// push onto unselected, remove from selected
			this.unselectedItems.push(this.selectedItems[i]);
			this.selectedItems.splice(i,1);

			// decrement pick counter
			this.pickCounter--;
		},

		// Submit choices for grading
		submitChoices(){

			// create array of items ordered by value high to low
			let orderedItems = this.selectedItems.concat(this.unselectedItems)
			orderedItems = orderedItems.sort( function(a, b){return b.market_price-a.market_price} )

			// figure out max possible value
			let maxValue = 0; 
			for(let i = 0; i < this.pickLimit; i++){
				// should trader price be considered?  currently only looking at market price

				// pickLimit cannot be larger than itemCount/orderedItems.length, so no index errors will occur
				maxValue += orderedItems[i].market_price
			}

			// get selectedItems value
			let selectedValue = 0;
			for(let i = 0; i < this.selectedItems.length; i++){
				selectedValue += this.selectedItems[i].market_price
			}

			// check to see if player won or lost
			if(selectedValue == maxValue){
				alert(`Congrats!  You won, value of selected items is ₽${selectedValue}`)
			} else {
				alert(`Sorry, you lose.  
					 \nMax possible value: ₽${maxValue} 
					 \nSelected Value: ₽${selectedValue}
					 \nDelta: ₽${maxValue - selectedValue}`)
			}

			// reset game
			this.generateItems()

		},


	},  // end methods
	computed: {

		// calculate number of picks reminaing
		picksRemaining(){
			return this.pickLimit - this.pickCounter
		},

	},   // end computed   
	mounted(){

		// when page is mounted, retrieve all item info from backend
		axios({
			method: 'get',
			url: `${this.$store.getters.backendEndpoints.api}/items/`,
		})
		.then(response => {
			
			// store response
			this.allItems = response.data

			// initialize game when page loads
			this.generateItems()
		})
		.catch(error => {console.log(error)})


	},   // end mounted

}
</script>
