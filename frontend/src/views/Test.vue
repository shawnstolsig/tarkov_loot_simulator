<template>
	<v-container>
		<!-- Tarkov Market Lookup by String -->
		<v-row>
			<v-col cols="12">
				<v-card>

					<v-card-title>
						Tarkov Market Item Lookup
					</v-card-title>

					<v-card-text>
						<v-container>
							<!-- Item input field/button -->
							<v-row>
								<v-col cols='12' md='9'>
									<v-text-field
										label="Input"
										v-model="inputString"
									></v-text-field>
								</v-col>
								<v-col cols='12' md='3'>
									<v-btn @click="lookupItem">
										Fetch Market Info
									</v-btn>
								</v-col>
							</v-row>

							<!-- Text area for response -->
							<v-row>
								<v-textarea
									v-model="responseItem"
									auto-grow
									readonly
									solo
								></v-textarea>
							</v-row>
						</v-container>				
					</v-card-text>

				</v-card>
			</v-col>
		</v-row>

		<!-- Tarkov Market get all items -->
		<v-row>
			<v-col cols="12">
				<v-card>

					<v-card-title>
						All Tarkov Market Items
					</v-card-title>

					<v-card-text>
						<v-container>
							<!-- Item input field/button -->
							<v-row>
								<v-col cols='12'>
									<v-btn @click="getAllItems">
										Get all
									</v-btn>
									<v-btn @click="updateBackend">
										Post to DB
									</v-btn>
								</v-col>
							</v-row>

							<!-- Text area for response -->
							<v-row>
								<v-textarea
									v-model="responseAllString"
									auto-grow
									readonly
									solo
								></v-textarea>
							</v-row>
						</v-container>				
					</v-card-text>

				</v-card>
			</v-col>
		</v-row>
	</v-container>
</template>

<script>
import axios from 'axios'
import Bottleneck from 'bottleneck'

export default {
	name: 'Home',
	components: {
		
	},
	data(){
		return {
			inputString: null,
			responseItem: null,
			responseAllString: null,
			responseAllObj: null,
			image: '',
		}
	},  // end data
	methods: {

		// get item info from Tarkov Market API
		lookupItem(){
			console.log(`Pulling Tarkov Market for ${this.inputString}`)
			axios({
				method: 'get',
				url: this.$store.getters.marketEndpoints.item,
				params: {
					q: this.inputString,
				},
				headers: {'x-api-key': this.$store.getters.marketApiKey},
				
			})
			.then(res => {
				// Console messages
				console.log(`Tarkov Market Response for ${this.inputString}`)
				console.log(res)

				// Load each property seperated by newline
				if(res.data.length > 0 ){
					this.responseItem = '';
					for(let hit of res.data){
						for (let prop in hit){
							this.responseItem += `${prop}: ${hit[prop]}\n`
						}
						this.responseItem += '\n'
					}
				} else {
					this.responseItem = "No results found.";
				}
			})
			.catch(error => {console.log(error)})
		},

		// get all items from Tarkov Market APIthis.$store.getters.marketApiKey
		getAllItems(){
			console.log(`Pulling Tarkov Market for all items.`)
			axios({
				method: 'get',
				url: this.$store.getters.marketEndpoints.all,
				headers: {'x-api-key': this.$store.getters.marketApiKey},			
			})
			.then(res => {
				// Console messages
				console.log(`Tarkov Market Response for all items:`)
				console.log(res)

				// Load each property seperated by newline
				if(res.data.length > 0 ){
					
					// save data object
					this.responseAllObj = res.data

					// create string for display
					this.responseAllString = '';
					for(let hit of res.data){
						for (let prop in hit){
							this.responseAllString += `${prop}: ${hit[prop]}\n`
						}
						this.responseAllString += '\n'
					}
				} else {
					this.responseAllString = "No results found.";
				}
			})
			.catch(error => {console.log(error)})
		},
		
		// update backend 
		updateBackend(){

			// DEVELOPMENT: temporary counter for development.  Set how many objects to update to backend
			let itemCounter = 1900

			// A counter for displaying progress as item info is fetched
			let progressCount = 0

			// Tarkov Rate is limited to 300 request/min.  Using Bottleneck for rate limiting
			// Waiting 210 ms between requests results in ~285 requests per minute
			const limiter = new Bottleneck({
				minTime: 210
			});

			if(this.responseAllObj== null){
				alert("Please pull all items from Tarkov Market first.")
			} else {

				// iterate through all items previously retrieved
				for(let item of this.responseAllObj){

					// DEVELOPMENT:  For developing, so only small portion is pulled from Tarkov Market to test
					if(itemCounter == 0 ){
						break
					}
					itemCounter--;

					// Progress message
					if(progressCount % 100 == 0){
						console.log(`Completed ${progressCount}`)
					}

					// get item info from Tarkov Market by uid
					limiter.schedule(() => 
						axios({
							method: 'get',
							url: this.$store.getters.marketEndpoints.item,
							params: {
								uid: item.uid,
							},
							headers: {'x-api-key': this.$store.getters.marketApiKey},
							
						})
					)
					.then(res => {
						let pulledItem = res.data[0]
						// console.log(`Retrieved ${pulledItem.name}:`)
						// console.log(res)

						// post item to backend
						return axios({
							method: 'post',
							url: `${this.$store.getters.backendEndpoint}/items/`,
							data: {
								uuid: pulledItem.uid,
								long_name: pulledItem.name,
								short_name: pulledItem.shortName,
								market_price: pulledItem.avg24hPrice,
								trader_price: pulledItem.traderPrice,
								trader_name: pulledItem.traderName,
								trader_currency: pulledItem.traderPriceCur,
								slots: pulledItem.slots,
								image_url: pulledItem.img,
								wiki_url: pulledItem.wikiLink,
								market_url: `https://tarkov-market.com/item/${pulledItem.name.toLowerCase().split(' ').join('_')}`
							}
						})
					})
					.then(() => {
						progressCount++
						console.log(`${progressCount}. Wrote/updated ${item.name} to db:`)

						// console.log(res)
					})
					.catch(error => {console.log(error)})
				}
			
			}
		},

	},  // end methods
	computed: {
	
	}   // end computed   

}
</script>
