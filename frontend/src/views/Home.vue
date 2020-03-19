<template>
	<v-container>

		<!-- Navigation drawer for game info -->
		<v-navigation-drawer permanent app clipped>
			<v-list-item>
				<v-list-item-content>
					<v-list-item-title class="title">
						Game Results
					</v-list-item-title>
				</v-list-item-content>
			</v-list-item>

			<v-divider></v-divider>

			<v-list	dense nav>

				<!-- Correct round counter -->
				<v-list-item>
					<v-list-item-icon>
						<v-icon>mdi-check-outline</v-icon>
					</v-list-item-icon>

					<v-list-item-content>
						<v-list-item-title>Correct</v-list-item-title>
						<v-list-item-subtitle>{{ winCount }}</v-list-item-subtitle>
					</v-list-item-content>
				</v-list-item>

				<!-- Incorrect round counter -->
				<v-list-item>
					<v-list-item-icon>
						<v-icon>mdi-close-outline</v-icon>
					</v-list-item-icon>

					<v-list-item-content>
						<v-list-item-title>Incorrect</v-list-item-title>
						<v-list-item-subtitle>{{ lossCount }}</v-list-item-subtitle>
					</v-list-item-content>
				</v-list-item>

				<!-- Money Gained Counter -->
				<v-list-item>
					<v-list-item-icon>
						<v-icon>mdi-trending-up</v-icon>
					</v-list-item-icon>

					<v-list-item-content>
						<v-list-item-title>Money Gained</v-list-item-title>
						<v-list-item-subtitle>{{ rublesGained }}</v-list-item-subtitle>
					</v-list-item-content>
				</v-list-item>

				<!-- Money Lost Counter -->
				<v-list-item>
					<v-list-item-icon>
						<v-icon>mdi-trending-down</v-icon>
					</v-list-item-icon>

					<v-list-item-content>
						<v-list-item-title>Money Lost</v-list-item-title>
						<v-list-item-subtitle>{{ rublesLost }}</v-list-item-subtitle>
					</v-list-item-content>
				</v-list-item>

				<!-- Efficiency -->
				<v-list-item>
					<v-list-item-icon>
						<v-icon>mdi-percent</v-icon>
					</v-list-item-icon>

					<v-list-item-content>
						<v-list-item-title>Efficiency</v-list-item-title>
						<v-list-item-subtitle>{{ efficiencyPercentage }}</v-list-item-subtitle>
					</v-list-item-content>
				</v-list-item>

				<v-divider></v-divider>
				
				<!-- Settings -->
				<v-list-item link @click="settingsDialog = true">
					<v-list-item-icon>
						<v-icon>mdi-cog</v-icon>
					</v-list-item-icon>

					<v-list-item-content>
						<v-list-item-title>Settings...</v-list-item-title>
					</v-list-item-content>
				</v-list-item>

				<v-dialog v-model="settingsDialog" width="500">

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

								<v-text-field
									label="Max Item Value"
									v-model="maxValue"
									type="number"
									:min='minValue + 1'
									append-icon="mdi-currency-rub"
								></v-text-field>

								<v-text-field
									label="Min Item Value"
									v-model="minValue"
									type="number"
									min='0'
									:max="maxValue - 1"
									append-icon="mdi-currency-rub"
								></v-text-field>

							</v-card-text>

							<v-divider></v-divider>

							<v-card-actions>
								<v-spacer></v-spacer>
								<v-btn	color="primary"	text @click="saveSettings">
									Close
								</v-btn>
							</v-card-actions>
						</v-card>
					</v-dialog>
			</v-list>
		</v-navigation-drawer>

		<!-- Items -->
		<v-row 
			v-for="item in thisRoundItems" 
			:key="item.id" 
			no-gutters
			align="center"
			justify="center"
			>

			<v-spacer></v-spacer>
			<!-- left side: unselected items -->
			<v-col cols="2">
				<v-tooltip bottom open-delay='500' v-if="unselectedItems.includes(item)">
					<template v-slot:activator="{ on }">
						<img :src="item.image_url" v-on="on" @click="moveToSelected(item)"/>
					</template>
					<span>{{ item.long_name }}</span>
				</v-tooltip>	
			</v-col>
			
			<v-spacer></v-spacer>

			<!-- right side: selected items -->
			<v-col cols="2">
				<v-tooltip bottom open-delay='500' v-if="selectedItems.includes(item)">
					<template v-slot:activator="{ on }">
						<img :src="item.image_url" v-on="on" @click="moveToUnselected(item)"/>
					</template>
					<span>{{ item.long_name }}</span>
				</v-tooltip>	
			</v-col>

			<v-spacer></v-spacer>

			<!-- Show values after submitting answers -->
			<v-col cols="2">
				<v-chip v-if="showValues" :color="correctItems.includes(item) ? 'success' : 'error'" :href="item.wiki_url" target="_blank">
					{{ showRubles(item.market_price) }}
				</v-chip>
			</v-col>

		</v-row>

		<!-- Submit button -->
		<v-row>
			<v-spacer></v-spacer>
			<v-col cols="1">
				<v-btn 
				@click="submitChoices" 
				:disabled="submitDisabled" 
				:color="buttonColor">
					{{showValues ? "Next" : "Submit"}}
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
			maxValue: 1000000000,
			minValue: 0,			

			// game data
			allItems: [],
			thisRoundItems: [],
			unselectedItems: [],
			selectedItems: [],
			correctItems: [],
			showValues: false,
			buttonColor: '',

			// for nav drawer
			winCount: 0,
			lossCount: 0,
			moneyLost: 0,
			moneyGained: 0,
		}
	},  // end data
	methods: {

		// Generate random items
		generateItems(){
			// reset game data
			this.showValues = false;
			this.thisRoundItems = [];
			this.unselectedItems = [];
			this.selectedItems = [];
			this.correctItems = [];
			this.pickCounter = 0;
			this.buttonColor = '';

			// loop through req'd num of items
			for(let i = 0; i < parseInt(this.itemCount); i++){

				// push an item at random from allItems
				let item = this.allItems[Math.floor(Math.random()*this.allItems.length)]
				
				// reselect item if image is null
				while(item.image_url == ''){
					console.log(`${item.long_name} doesn't have an image, reselecting`)
					item = this.allItems[Math.floor(Math.random()*this.allItems.length)]
				}

				// reselect item if item has already selected
				while(this.thisRoundItems.includes(item)){
					console.log(`${item.long_name} already selected, reselecting`)
					item = this.allItems[Math.floor(Math.random()*this.allItems.length)]
				}

				// reselect item if item is over maxValue or under minValue
				while(item.market_price > this.maxValue || item.market_price < this.minValue){
					console.log(`${item.long_name} is outside value range, reselecting`)
					item = this.allItems[Math.floor(Math.random()*this.allItems.length)]
				}

				// push item, once satisfactory item has been found
				this.unselectedItems.push(item)
				this.thisRoundItems.push(item)
			}
		},

		// Move from unselected to selected
		moveToSelected(item){

			// if showing values, then round is over...on click, redirect to items wiki page
			if(this.showValues){
				window.open(item.wiki_url, '_blank');
			} else {
				// if limit is reached, remove last item first
				if(this.picksRemaining == 0){
					// remove last item
					this.unselectedItems.push(this.selectedItems.pop())
					this.pickCounter--;
				} 

				// push onto selected, remove from unselected
				this.selectedItems.push(item);
				this.unselectedItems = this.unselectedItems.filter(i => i.uuid != item.uuid);

				// increment pick counter
				this.pickCounter++;
			}
		},

		// Move from selected to unselected
		moveToUnselected(item){

			// if showing values, then round is over...on click, redirect to items wiki page
			if(this.showValues){
				window.open(item.wiki_url, '_blank');
			} else {
				// push onto unselected, remove from selected
				this.unselectedItems.push(item);
				this.selectedItems = this.selectedItems.filter(i => i.uuid != item.uuid);

				// decrement pick counter
				this.pickCounter--;
			}
		},

		// Submit choices for grading
		submitChoices(){

			// if showing answer
			if (this.showValues){
				// reset game
				this.generateItems()
			} 
			// if not showing answers
			else {

				// create array of items ordered by value high to low
				let orderedItems = this.selectedItems.concat(this.unselectedItems)
				orderedItems = orderedItems.sort( function(a, b){return b.market_price-a.market_price} )

				// figure out max possible value
				let maxValue = 0; 
				for(let i = 0; i < this.pickLimit; i++){
					// should trader price be considered?  currently only looking at market price

					// pickLimit cannot be larger than itemCount/orderedItems.length, so no index errors will occur
					maxValue += orderedItems[i].market_price;
					this.correctItems.push(orderedItems[i]);
				}

				// get selectedItems value
				let selectedValue = 0;
				for(let i = 0; i < this.selectedItems.length; i++){
					selectedValue += this.selectedItems[i].market_price
				}

				// add selected values to money gained
				this.moneyGained += selectedValue

				// check to see if player won or lost
				if(selectedValue == maxValue){
					this.buttonColor = 'success';
					this.winCount++;
				} else {
					this.buttonColor = 'error';
					this.lossCount++;
					let delta = maxValue - selectedValue
					this.moneyLost += delta
				}

				// show item values
				this.showValues = true;
			}
		},

		// save settings 
		saveSettings(){

			// close dialog
			this.settingsDialog = false

			// reset game
			this.generateItems()
		},

		// helper for converting to rubles
		showRubles(n){
			return new Intl.NumberFormat('ru-RU', { style: 'currency', currency: 'RUB', minimumFractionDigits: 0 }).format(n)
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

		// compute efficiency of selections 
		efficiencyPercentage(){
			let ratio = this.moneyGained / (this.moneyGained + this.moneyLost)
			if(isNaN(ratio)){
				return '-'
			} 
			return (ratio*100).toFixed(1) + '%'
		},

        // show rubles gained
		rublesGained(){
			return this.showRubles(this.moneyGained)
		},

		// show rubles lost
		rublesLost(){
			return this.showRubles(this.moneyLost)
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
	watch: {

		// automatically lower maxPickLimit if itemCount drops to pick limit
		itemCount: function(val){
			if (val == this.pickLimit){
				this.pickLimit--
			}
		},

		// automatically raise maxLimit if minValue is >= maxValue
		minValue: function(val){
			val = parseInt(val)
			if(val >= this.maxValue){
				this.maxValue = val + 1
			}
		},
		
		// automatically lower minValue if maxValue is <= maxValue
		maxValue: function(val){
			val = parseInt(val)
			if(val <= this.minValue){
				this.minValue = this.maxValue - 1
			}
			if(val <= 1){
				this.minValue = 0
				this.maxValue = 1
			}
		},
	}, 	 // end watch

}
</script>
