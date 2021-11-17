<template>
  <b-container>
    <h1 class="mt-5">Multiply matrix times itself</h1>
    <div class="mt-4">
      <b-button 
        class="mx-2" 
        :disabled="currentN <= lowLimit" 
        @click="reduce()"
      >
        <i class="fas fa-angle-left"></i>
      </b-button>
      <b-button 
        class="mx-1" 
        @click="randomize()"
      >
        <i class="fas fa-random"></i>
      </b-button>
      <b-button 
        class="mx-1" 
        @click="solve()"
      >
        <i class="fas fa-calculator"></i>
      </b-button>
      <b-button 
        class="mx-2" 
        :disabled="currentN >= highLimit" 
        @click="increase()"
      >
        <i class="fas fa-angle-right"></i>
      </b-button>
    </div>
    <b-table 
      class="mt-5"
      style="border:2px solid black"
      thead-class="hidden_header"
      :items="inputItems"
      bordered 
      responsive 
    ></b-table>
    <b-modal 
      id="solution-modal" 
      size="xl" 
      title="Solution"
      centered
      hide-header-close
      ok-only
    >
      <b-table 
        style="border:2px solid black"
        thead-class="hidden_header"
        :items="outputItems"
        bordered 
        responsive
      ></b-table>

      <span>Solved in <b>{{time}} seconds</b></span>
    </b-modal>
  </b-container>
</template>

<script>
import { getDatabase, ref, onValue, set } from "firebase/database";
import _ from "lodash";

export default {
  name: 'Home',
  data() {
    return {
      inputItems: [],
      outputItems: [],
      currentN: 3,
      lowLimit: 2,
      highLimit: 10,
      time: 0
    }
  },
  methods: {
    formatTable(matrix) {
      this.outputItems = [];
      matrix.forEach((r, i) => {
        let row = {};
        matrix[i].forEach((e, j) => {
          row[j] = e
        })
        this.outputItems.push(row);
      });
    },
    formatMatrix(table) {
      let matrix = []
      table.forEach((r, i) => {
        let row = [];
        _.keys(r).forEach(k => {
          row.push(table[i][k])
        })
        matrix.push(row);
      })
      return matrix;
    },
    reduce() {
      if(this.currentN <= this.lowLimit) return;
      this.currentN -= 1;
      this.randomize();
    },
    increase() {
      if(this.currentN >= this.highLimit) return;
      this.currentN += 1;
      this.randomize();
    },
    randomize() {
      let min = 1;
      let max = 101;
      this.inputItems = [];
      for(let i = 0; i < this.currentN; i++) {
        let row = {};
        for(let j = 0; j < this.currentN; j++) {
          row[j] = Math.floor(Math.random() * (max - min)) + min;
        }
        this.inputItems.push(row);
      }
    },
    solve() {
      const inputMatrix = this.formatMatrix(this.inputItems)
      const db = getDatabase();
      const inputRef = ref(db, 'input');
      set(inputRef, inputMatrix);
      this.$bvModal.show("solution-modal")
    }
  },
  mounted() {
    this.randomize();
    const db = getDatabase();
    const outputRef = ref(db, 'output');
    onValue(outputRef, (snapshot) => {
      const data = snapshot.val();
      const matrix = _.get(data, 'matrix', []);
      this.time = _.get(data, 'time', 0);
      this.formatTable(matrix);
    }); 
  }
}
</script>

<style>
.hidden_header {
  display: none;
}
</style>
