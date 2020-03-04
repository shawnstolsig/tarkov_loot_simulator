<template>
    <nav>
        <v-app-bar app>
            
            <!-- Site logo/title -->
            <v-toolbar-title>
                <span class="title">EFT: Loot Trainer</span>
            </v-toolbar-title>

            <v-spacer></v-spacer>
        
            <!-- Toolbar buttons -->
            <v-toolbar-items>
                <v-btn text to="/" class="mr-2">
                    <span>Home</span>
                    <v-icon right>mdi-home</v-icon>
                </v-btn>
                <v-btn text to="/about" class="mr-2">
                    <span>About</span>
                    <v-icon right >mdi-information</v-icon>
                </v-btn>
            </v-toolbar-items>
        </v-app-bar>
    </nav>
</template>


<script>


export default {
    data(){
        return {
         
        }
    },  // end data
    methods: {
        
    },  // end methods
    computed: {
       
    }   // end computed
}
</script>