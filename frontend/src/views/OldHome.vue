<template>
	<v-container>


		<!-- Settings button, column labels-->
		<v-card>

		
			<v-row>
				<v-col cols="2" md="2" >
					<v-dialog v-model="settingsDialog" width="500">
						<template v-slot:activator="{ on }">
							<v-btn icon v-on="on" dark>
								<v-icon >mdi-cog</v-icon>
							</v-btn>
						</template>

						<v-card>
							<v-card-title class="title" primary-title>
								Game Settings
							</v-card-title>

							<v-card-text>
								<v-text-field
									label="Number of items"
									v-model="itemCount"
									type="number"
									min='2'
									max='300'
								></v-text-field>

								<v-text-field
									label="Number of choices"
									v-model="pickLimit"
									type="number"
									min='1'
									:max="maxPickLimit"
								></v-text-field>

							</v-card-text>

							<v-divider></v-divider>

							<v-card-actions>
								<v-spacer></v-spacer>
								<v-btn	color="primary"	text @click="saveSettings">
									Save
								</v-btn>
							</v-card-actions>
						</v-card>
					</v-dialog>
				</v-col>


				<v-col cols="2" md="2">
					<v-text-field
						readonly
						label="Wins"
						v-model="winCount"
						outlined
					></v-text-field>
				</v-col>

				<v-col cols="2" md="2">
					<v-text-field
						readonly
						label="Losses"
						v-model="lossCount"
						outlined
					></v-text-field>
				</v-col>

				<v-col cols="2" md="2">
					<v-text-field
						readonly
						label="Money Gained"
						v-model="moneyGainedFormatted"
						outlined
					></v-text-field>
				</v-col>

				<v-col cols="2" md="2">
					<v-text-field
						readonly
						label="Money Lost"
						v-model="moneyLostFormatted"
						outlined
					></v-text-field>
				</v-col>

				<v-col cols="2" md="2">
					<v-text-field
						readonly
						label="Efficiency"
						v-model="efficiencyPercentage"
						outlined
					></v-text-field>
				</v-col>

			</v-row>
		</v-card>




		<!-- Items -->
		<v-row>
			<v-spacer></v-spacer>
			<!-- Right side: unselected items -->
			<v-col cols="6">
				<v-tooltip 
					bottom 
					open-delay='500' 
					v-for="i in selectedItems.length" 
					:key="i">
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
				<v-btn @click="submitChoices" :disabled="submitDisabled">
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
			settingsDialog: false,
			itemCount: 6,
			pickLimit: 1,
			pickCounter: 0,			

			// game data
			allItems: [],
			unselectedItems: [],
			selectedItems: [],
			winCount: 0,
			lossCount: 0,
			moneyLostFormatted: 0,
			moneyGainedFormatted: 0,
			moneyLostCalculated: 0,
			moneyGainedCalculated: 0,

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
				
				// reselect item if image is null
				while(item.image_url == ''){
					console.log(`${item.long_name} doesn't have an image, reselecting`)
					item = this.allItems[Math.floor(Math.random()*this.allItems.length)]
				}
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

			// add selected values to money gained
			this.moneyGainedCalculated += selectedValue

			// check to see if player won or lost
			if(selectedValue == maxValue){
				this.winCount++;
			} else {
				this.lossCount++;
				let delta = maxValue - selectedValue
				this.moneyLostCalculated += delta
			}

			// update the currency-formatted numbers
			this.moneyGainedFormatted = new Intl.NumberFormat('ru-RU', { style: 'currency', currency: 'RUB', minimumFractionDigits: 0 }).format(this.moneyGainedCalculated)
			this.moneyLostFormatted = new Intl.NumberFormat('ru-RU', { style: 'currency', currency: 'RUB', minimumFractionDigits: 0 }).format(this.moneyLostCalculated)

			// reset game
			this.generateItems()
		},

		// save settings 
		saveSettings(){

			// close dialog
			this.settingsDialog = false

			// reset game
			this.generateItems()
		},


	},  // end methods
	computed: {

		// calculate number of picks reminaing
		picksRemaining(){
			return this.pickLimit - this.pickCounter
		},

		// max pick limit is one less than item count
		maxPickLimit(){
			return this.itemCount - 1
		},

		// figure out if all picks have been used before enabling button
		submitDisabled(){
			return this.selectedItems.length != this.pickLimit
		},

		efficiencyPercentage(){
			let ratio = this.moneyGainedCalculated / (this.moneyGainedCalculated + this.moneyLostCalculated)
			if(isNaN(ratio)){
				return '-'
			} 
			return (ratio*100).toFixed(1) + '%'
		}

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
	watch: {

		// automatically lower maxPickLimit if itemCount drops to pick limit
		itemCount: function(val){
			if (val == this.pickLimit){
				this.pickLimit--
			}
		}
	}, 	 // end watch

}
</script>
