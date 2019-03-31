<template>
  <div class="hello">
    <h1>Body Mass Index (BMI) and Body Surface Area (BSA)</h1>
    <p>Calculates body mass index and body surface area.</p>
    <div class="inputs">
      <section>
        <div>Weight</div>
        <div>
          <input type="number" min="45" max="113">
          <button>kg</button>
        </div>
      </section>
      <section>
        <div>Height</div>
        <div>
          <input type="number" min="30" max="250">
          <button>cm</button>
        </div>
      </section>
    </div>
    <div class="results">
      <section>
        <div>BMI</div>
        <div>
          <label>BMI:</label>
          <span>21</span>
        </div>
      </section>
    </div>
  </div>
</template>

<script>
export default {
  name: "HelloWorld",
  props: {
    msg: String
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.inputs section {
  display: block;
  clear: both;
  margin-top: .1em;
  margin-bottom: .1em;
  border-bottom: 1px solid #f0f0f0;
  border-top: 1px solid #f0f0f0;
}
.inputs section::after {
  display: block;
  clear: both;
  content: " ";
}
.inputs section div:first-child {
  width: 50%;
  float: left;
}
.inputs section div:last-child {
  width: 50%;
  float: right;
}
</style>
