<script setup lang="ts">
    import router from "@/router";
    const medications = [
        {
            name: "Paracetamol",
            description:
                "Paracetamol is a widely used painkiller and fever reducer. It treats headaches, toothaches, and minor aches. It is safe for most users when taken as directed. Overuse can lead to liver damage. Available in tablets, syrup, and suppository forms for both adults and children.",
        },
        {
            name: "Ibuprofen",
            description:
                "Ibuprofen is a non-steroidal anti-inflammatory drug (NSAID) used for pain, inflammation, and fever. It’s effective for menstrual cramps, arthritis, and muscle aches. Best taken with food to reduce stomach irritation. Available in tablets and suspension forms. Not suitable for people with ulcers or kidney issues.",
        },
        {
            name: "Amoxicillin",
            description:
                "Amoxicillin is a penicillin antibiotic used to treat bacterial infections like ear infections, pneumonia, and urinary tract infections. It works by stopping the growth of bacteria. Always complete the prescribed course. Not effective against viral infections. May cause mild side effects like nausea or rash.",
        },
        {
            name: "Cetirizine",
            description:
                "Cetirizine is an antihistamine that relieves allergy symptoms such as runny nose, sneezing, and itchy eyes. It’s commonly used for hay fever and skin hives. Non-drowsy in most people. Works within an hour and lasts up to 24 hours. Safe for adults and children over six.",
        },
        {
            name: "Metformin",
            description:
                "Metformin is an oral medication for managing type 2 diabetes. It helps control blood sugar levels by improving insulin sensitivity and reducing liver glucose production. Taken with meals to reduce stomach upset. Not for type 1 diabetes. Regular monitoring of kidney function is advised during long-term use.",
        },
        {
            name: "Loratadine",
            description:
                "Loratadine is a non-drowsy antihistamine used to treat allergy symptoms like sneezing, itchy eyes, and runny nose. Suitable for both adults and children. Typically taken once daily. Relief starts within an hour. Not recommended during pregnancy without medical advice. Available in tablets, syrup, and dissolvable forms.",
        },
        {
            name: "Azithromycin",
            description:
                "Azithromycin is a macrolide antibiotic used to treat bacterial infections like bronchitis, pneumonia, and certain STDs. It works by preventing bacteria from growing. Often prescribed in short courses. Take on an empty stomach for better absorption. Can cause mild gastrointestinal upset or temporary changes in taste.",
        },
        {
            name: "Omeprazole",
            description:
                "Omeprazole reduces stomach acid and treats conditions like ulcers, GERD, and acid reflux. It belongs to the proton pump inhibitor (PPI) class. Best taken before meals. Long-term use may affect calcium and magnesium levels. Available over-the-counter or by prescription. Improves symptoms within a few days of use.",
        },
        {
            name: "Salbutamol",
            description:
                "Salbutamol is a bronchodilator used to relieve asthma and chronic obstructive pulmonary disease (COPD) symptoms. It quickly opens airways to ease breathing. Usually inhaled via inhaler or nebulizer. Works within minutes. Not a long-term controller—used for quick relief. Side effects may include tremors or increased heart rate.",
        },
        {
            name: "Diphenhydramine",
            description:
                "Diphenhydramine is a sedating antihistamine used to treat allergies, insomnia, and motion sickness. It provides quick relief for sneezing, itching, and hives. Also used as a nighttime sleep aid. Causes drowsiness, so avoid driving. Available in tablets, capsules, and syrups. Not recommended for children under two years.",
        },
        {
            name: "Lisinopril",
            description:
                "Lisinopril is an ACE inhibitor used to treat high blood pressure and heart failure. It helps relax blood vessels, improving blood flow. Regular use reduces stroke and heart attack risk. Taken once daily. Side effects may include dizziness or cough. Not safe during pregnancy. Requires regular blood pressure monitoring.",
        },
        {
            name: "Amlodipine",
            description:
                "Amlodipine is a calcium channel blocker used to treat high blood pressure and angina. It relaxes blood vessels to improve blood flow and reduce heart workload. Taken daily, with or without food. May cause swelling or dizziness. Gradual onset—results appear over days. Do not stop abruptly without advice.",
        },
        {
            name: "Hydrochlorothiazide",
            description:
                "Hydrochlorothiazide is a diuretic used to treat high blood pressure and fluid retention. It helps the body eliminate excess salt and water. Best taken in the morning. Can cause increased urination, dizziness, or electrolyte imbalance. Regular blood tests recommended. Works well as part of combination therapy for hypertension.",
        },
        {
            name: "Clopidogrel",
            description:
                "Clopidogrel is an antiplatelet drug that prevents blood clots in patients with heart disease, stroke risk, or after certain surgeries. It helps maintain blood flow in arteries. Taken once daily. Do not stop without doctor’s advice. May cause bleeding or bruising. Avoid alcohol and NSAIDs while on treatment.",
        },
        {
            name: "Folic Acid",
            description:
                "Folic acid is a vitamin essential for red blood cell production and fetal development during pregnancy. It prevents neural tube defects and treats folate deficiency anemia. Often prescribed for pregnant women. Usually well tolerated. Taken once daily with or without food. Available alone or in prenatal multivitamin combinations.",
        },
        {
            name: "Prednisolone",
            description:
                "Prednisolone is a corticosteroid used to reduce inflammation in conditions like asthma, arthritis, and allergic reactions. It suppresses the immune response and relieves swelling. Must be taken as prescribed and tapered gradually. Side effects include mood changes, weight gain, and increased blood sugar. Not recommended for long-term unsupervised use.",
        },
        {
            name: "Diazepam",
            description:
                "Diazepam is a benzodiazepine used to relieve anxiety, muscle spasms, and seizures. It also treats alcohol withdrawal symptoms. Has a calming effect on the brain. Can cause drowsiness or dependence if misused. Prescribed for short-term use only. Avoid alcohol while taking diazepam. Should not be stopped abruptly.",
        },
        {
            name: "Simvastatin",
            description:
                "Simvastatin is a cholesterol-lowering medication used to reduce the risk of heart disease and stroke. It works by decreasing LDL (bad) cholesterol and increasing HDL (good) cholesterol. Taken at night, often once daily. May cause muscle pain or liver issues. Regular monitoring of cholesterol and liver function is advised.",
        },
        {
            name: "Insulin",
            description:
                "Insulin is a hormone therapy used to control blood sugar in people with diabetes, especially type 1. Administered via injection or pump. Different types vary in onset and duration. Essential for managing glucose levels. Requires careful dosage and monitoring to avoid hypoglycemia. Diet and exercise should be coordinated accordingly.",
        },
        {
            name: "Codeine",
            description:
                "Codeine is a mild opioid used to treat moderate pain and persistent cough. It works by altering pain perception in the brain. May cause drowsiness, constipation, or dependency. Often combined with paracetamol. Should not be used in children under 12. Avoid alcohol and driving while taking codeine-containing medications.",
        },
        {
            name: "Ciprofloxacin",
            description:
                "Ciprofloxacin is a broad-spectrum antibiotic used to treat infections like UTIs, respiratory issues, and gastrointestinal infections. Belongs to the fluoroquinolone class. Not suitable for children or pregnant women. Can cause tendon problems or photosensitivity. Take with water and avoid dairy or calcium-rich products close to dosage time.",
        },
        {
            name: "Levothyroxine",
            description:
                "Levothyroxine is a thyroid hormone replacement used to treat hypothyroidism. It normalizes metabolism and energy levels. Taken on an empty stomach, usually in the morning. Requires regular blood tests for dose adjustment. Do not switch brands without consulting a doctor. Overdose may cause rapid heartbeat, insomnia, or anxiety.",
        },
        {
            name: "Ranitidine",
            description:
                "Ranitidine is an H2 blocker that reduces stomach acid, treating ulcers, GERD, and heartburn. It offers quick symptom relief. Taken once or twice daily. Avoid long-term use without medical supervision. Due to safety concerns, some countries have restricted its use. Alternatives like famotidine are often recommended now.",
        },
        {
            name: "Iron Sulfate",
            description:
                "Iron sulfate is a supplement used to treat or prevent iron-deficiency anemia. It helps the body produce healthy red blood cells. Best absorbed on an empty stomach, but may cause nausea or constipation. Vitamin C improves absorption. Long-term use should be monitored to avoid iron overload or toxicity.",
        },
        {
            name: "Warfarin",
            description:
                "Warfarin is a blood thinner used to prevent and treat blood clots in conditions like deep vein thrombosis and atrial fibrillation. Dosage is closely monitored with blood tests (INR). Avoid sudden changes in diet, especially with vitamin K-rich foods. Interacts with many drugs. Requires consistent follow-up and caution.",
        },
        {
            name: "Prednisolone",
            description:
                "Prednisolone is a corticosteroid used to reduce inflammation in conditions like asthma, arthritis, and allergic reactions. It suppresses the immune response and relieves swelling. Must be taken as prescribed and tapered gradually. Side effects include mood changes, weight gain, and increased blood sugar. Not recommended for long-term unsupervised use.",
        },
        {
            name: "Diazepam",
            description:
                "Diazepam is a benzodiazepine used to relieve anxiety, muscle spasms, and seizures. It also treats alcohol withdrawal symptoms. Has a calming effect on the brain. Can cause drowsiness or dependence if misused. Prescribed for short-term use only. Avoid alcohol while taking diazepam. Should not be stopped abruptly.",
        },
        {
            name: "Simvastatin",
            description:
                "Simvastatin is a cholesterol-lowering medication used to reduce the risk of heart disease and stroke. It works by decreasing LDL (bad) cholesterol and increasing HDL (good) cholesterol. Taken at night, often once daily. May cause muscle pain or liver issues. Regular monitoring of cholesterol and liver function is advised.",
        },
        {
            name: "Insulin",
            description:
                "Insulin is a hormone therapy used to control blood sugar in people with diabetes, especially type 1. Administered via injection or pump. Different types vary in onset and duration. Essential for managing glucose levels. Requires careful dosage and monitoring to avoid hypoglycemia. Diet and exercise should be coordinated accordingly.",
        },
        {
            name: "Codeine",
            description:
                "Codeine is a mild opioid used to treat moderate pain and persistent cough. It works by altering pain perception in the brain. May cause drowsiness, constipation, or dependency. Often combined with paracetamol. Should not be used in children under 12. Avoid alcohol and driving while taking codeine-containing medications.",
        },
        {
            name: "Ciprofloxacin",
            description:
                "Ciprofloxacin is a broad-spectrum antibiotic used to treat infections like UTIs, respiratory issues, and gastrointestinal infections. Belongs to the fluoroquinolone class. Not suitable for children or pregnant women. Can cause tendon problems or photosensitivity. Take with water and avoid dairy or calcium-rich products close to dosage time.",
        },
        {
            name: "Levothyroxine",
            description:
                "Levothyroxine is a thyroid hormone replacement used to treat hypothyroidism. It normalizes metabolism and energy levels. Taken on an empty stomach, usually in the morning. Requires regular blood tests for dose adjustment. Do not switch brands without consulting a doctor. Overdose may cause rapid heartbeat, insomnia, or anxiety.",
        },
        {
            name: "Ranitidine",
            description:
                "Ranitidine is an H2 blocker that reduces stomach acid, treating ulcers, GERD, and heartburn. It offers quick symptom relief. Taken once or twice daily. Avoid long-term use without medical supervision. Due to safety concerns, some countries have restricted its use. Alternatives like famotidine are often recommended now.",
        },
        {
            name: "Iron Sulfate",
            description:
                "Iron sulfate is a supplement used to treat or prevent iron-deficiency anemia. It helps the body produce healthy red blood cells. Best absorbed on an empty stomach, but may cause nausea or constipation. Vitamin C improves absorption. Long-term use should be monitored to avoid iron overload or toxicity.",
        },
        {
            name: "Warfarin",
            description:
                "Warfarin is a blood thinner used to prevent and treat blood clots in conditions like deep vein thrombosis and atrial fibrillation. Dosage is closely monitored with blood tests (INR). Avoid sudden changes in diet, especially with vitamin K-rich foods. Interacts with many drugs. Requires consistent follow-up and caution.",
        },
        {
            name: "Metformin",
            description:
                "Metformin is an oral medication for managing type 2 diabetes. It helps control blood sugar levels by improving insulin sensitivity and reducing liver glucose production. Taken with meals to reduce stomach upset. Not for type 1 diabetes. Regular monitoring of kidney function is advised during long-term use.",
        },
        {
            name: "Loratadine",
            description:
                "Loratadine is a non-drowsy antihistamine used to treat allergy symptoms like sneezing, itchy eyes, and runny nose. Suitable for both adults and children. Typically taken once daily. Relief starts within an hour. Not recommended during pregnancy without medical advice. Available in tablets, syrup, and dissolvable forms.",
        },
        {
            name: "Azithromycin",
            description:
                "Azithromycin is a macrolide antibiotic used to treat bacterial infections like bronchitis, pneumonia, and certain STDs. It works by preventing bacteria from growing. Often prescribed in short courses. Take on an empty stomach for better absorption. Can cause mild gastrointestinal upset or temporary changes in taste.",
        },
        {
            name: "Omeprazole",
            description:
                "Omeprazole reduces stomach acid and treats conditions like ulcers, GERD, and acid reflux. It belongs to the proton pump inhibitor (PPI) class. Best taken before meals. Long-term use may affect calcium and magnesium levels. Available over-the-counter or by prescription. Improves symptoms within a few days of use.",
        },
        {
            name: "Salbutamol",
            description:
                "Salbutamol is a bronchodilator used to relieve asthma and chronic obstructive pulmonary disease (COPD) symptoms. It quickly opens airways to ease breathing. Usually inhaled via inhaler or nebulizer. Works within minutes. Not a long-term controller—used for quick relief. Side effects may include tremors or increased heart rate.",
        },
        {
            name: "Diphenhydramine",
            description:
                "Diphenhydramine is a sedating antihistamine used to treat allergies, insomnia, and motion sickness. It provides quick relief for sneezing, itching, and hives. Also used as a nighttime sleep aid. Causes drowsiness, so avoid driving. Available in tablets, capsules, and syrups. Not recommended for children under two years.",
        },
        {
            name: "Lisinopril",
            description:
                "Lisinopril is an ACE inhibitor used to treat high blood pressure and heart failure. It helps relax blood vessels, improving blood flow. Regular use reduces stroke and heart attack risk. Taken once daily. Side effects may include dizziness or cough. Not safe during pregnancy. Requires regular blood pressure monitoring.",
        },
        {
            name: "Amlodipine",
            description:
                "Amlodipine is a calcium channel blocker used to treat high blood pressure and angina. It relaxes blood vessels to improve blood flow and reduce heart workload. Taken daily, with or without food. May cause swelling or dizziness. Gradual onset—results appear over days. Do not stop abruptly without advice.",
        },
        {
            name: "Hydrochlorothiazide",
            description:
                "Hydrochlorothiazide is a diuretic used to treat high blood pressure and fluid retention. It helps the body eliminate excess salt and water. Best taken in the morning. Can cause increased urination, dizziness, or electrolyte imbalance. Regular blood tests recommended. Works well as part of combination therapy for hypertension.",
        },
        {
            name: "Clopidogrel",
            description:
                "Clopidogrel is an antiplatelet drug that prevents blood clots in patients with heart disease, stroke risk, or after certain surgeries. It helps maintain blood flow in arteries. Taken once daily. Do not stop without doctor’s advice. May cause bleeding or bruising. Avoid alcohol and NSAIDs while on treatment.",
        },
        {
            name: "Folic Acid",
            description:
                "Folic acid is a vitamin essential for red blood cell production and fetal development during pregnancy. It prevents neural tube defects and treats folate deficiency anemia. Often prescribed for pregnant women. Usually well tolerated. Taken once daily with or without food. Available alone or in prenatal multivitamin combinations.",
        },
        {
            name: "Prednisolone",
            description:
                "Prednisolone is a corticosteroid used to reduce inflammation in conditions like asthma, arthritis, and allergic reactions. It suppresses the immune response and relieves swelling. Must be taken as prescribed and tapered gradually. Side effects include mood changes, weight gain, and increased blood sugar. Not recommended for long-term unsupervised use.",
        },
        {
            name: "Diazepam",
            description:
                "Diazepam is a benzodiazepine used to relieve anxiety, muscle spasms, and seizures. It also treats alcohol withdrawal symptoms. Has a calming effect on the brain. Can cause drowsiness or dependence if misused. Prescribed for short-term use only. Avoid alcohol while taking diazepam. Should not be stopped abruptly.",
        },
        {
            name: "Simvastatin",
            description:
                "Simvastatin is a cholesterol-lowering medication used to reduce the risk of heart disease and stroke. It works by decreasing LDL (bad) cholesterol and increasing HDL (good) cholesterol. Taken at night, often once daily. May cause muscle pain or liver issues. Regular monitoring of cholesterol and liver function is advised.",
        },
        {
            name: "Insulin",
            description:
                "Insulin is a hormone therapy used to control blood sugar in people with diabetes, especially type 1. Administered via injection or pump. Different types vary in onset and duration. Essential for managing glucose levels. Requires careful dosage and monitoring to avoid hypoglycemia. Diet and exercise should be coordinated accordingly.",
        },
        {
            name: "Codeine",
            description:
                "Codeine is a mild opioid used to treat moderate pain and persistent cough. It works by altering pain perception in the brain. May cause drowsiness, constipation, or dependency. Often combined with paracetamol. Should not be used in children under 12. Avoid alcohol and driving while taking codeine-containing medications.",
        },
        {
            name: "Ciprofloxacin",
            description:
                "Ciprofloxacin is a broad-spectrum antibiotic used to treat infections like UTIs, respiratory issues, and gastrointestinal infections. Belongs to the fluoroquinolone class. Not suitable for children or pregnant women. Can cause tendon problems or photosensitivity. Take with water and avoid dairy or calcium-rich products close to dosage time.",
        },
        {
            name: "Levothyroxine",
            description:
                "Levothyroxine is a thyroid hormone replacement used to treat hypothyroidism. It normalizes metabolism and energy levels. Taken on an empty stomach, usually in the morning. Requires regular blood tests for dose adjustment. Do not switch brands without consulting a doctor. Overdose may cause rapid heartbeat, insomnia, or anxiety.",
        },
        {
            name: "Ranitidine",
            description:
                "Ranitidine is an H2 blocker that reduces stomach acid, treating ulcers, GERD, and heartburn. It offers quick symptom relief. Taken once or twice daily. Avoid long-term use without medical supervision. Due to safety concerns, some countries have restricted its use. Alternatives like famotidine are often recommended now.",
        },
        {
            name: "Iron Sulfate",
            description:
                "Iron sulfate is a supplement used to treat or prevent iron-deficiency anemia. It helps the body produce healthy red blood cells. Best absorbed on an empty stomach, but may cause nausea or constipation. Vitamin C improves absorption. Long-term use should be monitored to avoid iron overload or toxicity.",
        },
        {
            name: "Warfarin",
            description:
                "Warfarin is a blood thinner used to prevent and treat blood clots in conditions like deep vein thrombosis and atrial fibrillation. Dosage is closely monitored with blood tests (INR). Avoid sudden changes in diet, especially with vitamin K-rich foods. Interacts with many drugs. Requires consistent follow-up and caution.",
        },
        {
            name: "Prednisolone",
            description:
                "Prednisolone is a corticosteroid used to reduce inflammation in conditions like asthma, arthritis, and allergic reactions. It suppresses the immune response and relieves swelling. Must be taken as prescribed and tapered gradually. Side effects include mood changes, weight gain, and increased blood sugar. Not recommended for long-term unsupervised use.",
        },
        {
            name: "Diazepam",
            description:
                "Diazepam is a benzodiazepine used to relieve anxiety, muscle spasms, and seizures. It also treats alcohol withdrawal symptoms. Has a calming effect on the brain. Can cause drowsiness or dependence if misused. Prescribed for short-term use only. Avoid alcohol while taking diazepam. Should not be stopped abruptly.",
        },
        {
            name: "Simvastatin",
            description:
                "Simvastatin is a cholesterol-lowering medication used to reduce the risk of heart disease and stroke. It works by decreasing LDL (bad) cholesterol and increasing HDL (good) cholesterol. Taken at night, often once daily. May cause muscle pain or liver issues. Regular monitoring of cholesterol and liver function is advised.",
        },
        {
            name: "Insulin",
            description:
                "Insulin is a hormone therapy used to control blood sugar in people with diabetes, especially type 1. Administered via injection or pump. Different types vary in onset and duration. Essential for managing glucose levels. Requires careful dosage and monitoring to avoid hypoglycemia. Diet and exercise should be coordinated accordingly.",
        },
        {
            name: "Codeine",
            description:
                "Codeine is a mild opioid used to treat moderate pain and persistent cough. It works by altering pain perception in the brain. May cause drowsiness, constipation, or dependency. Often combined with paracetamol. Should not be used in children under 12. Avoid alcohol and driving while taking codeine-containing medications.",
        },
        {
            name: "Ciprofloxacin",
            description:
                "Ciprofloxacin is a broad-spectrum antibiotic used to treat infections like UTIs, respiratory issues, and gastrointestinal infections. Belongs to the fluoroquinolone class. Not suitable for children or pregnant women. Can cause tendon problems or photosensitivity. Take with water and avoid dairy or calcium-rich products close to dosage time.",
        },
        {
            name: "Levothyroxine",
            description:
                "Levothyroxine is a thyroid hormone replacement used to treat hypothyroidism. It normalizes metabolism and energy levels. Taken on an empty stomach, usually in the morning. Requires regular blood tests for dose adjustment. Do not switch brands without consulting a doctor. Overdose may cause rapid heartbeat, insomnia, or anxiety.",
        },
    ];
</script>

<template>
    <div class="h-screen w-full relative flex flex-col flex-1 overflow-hidden">
        <div
            class="hidden md:flex md:justify-between md:items-center w-full md:absolute top-0 z-50 p-3 bg-gray-900"
        >
            <h1
                class="text-gray-300 font-styleScript text-center text-lg md:text-2xl"
            >
                Meds Jane Doe
            </h1>
            <div>
                <form
                    @submit.prevent=""
                    class="flex items-center justify-between gap-4 text-white"
                >
                    <input
                        type="text"
                        placeholder="Search medications"
                        class="block mx-auto border border-gray-400 rounded outline-none focus:border-orange-700 h-9 px-4 md:h-10 bg-transparent"
                    />
                    <button
                        type="submit"
                        class="bg-orange-600 hover:bg-orange-500 text-white font-bold py-2 px-4 rounded"
                    >
                        <i class="pi pi-search"></i>
                    </button>
                </form>
            </div>
        </div>
        <div class="overflow-y-auto overscroll-contain w-full mb-14 md:mb-0">
            <div class="mx-auto container md:pt-16">
                <div class="md:hidden p-3 pb-0">
                    <form
                        @submit.prevent=""
                        class="flex items-center justify-between gap-4"
                    >
                        <input
                            type="text"
                            placeholder="Search medications"
                            class="block mx-auto border border-gray-400 rounded outline-none focus:border-orange-700 h-9 px-4 md:h-10 bg-transparent"
                        />
                        <button
                            type="submit"
                            class="bg-orange-600 hover:bg-orange-500 text-white font-bold py-2 px-4 rounded"
                        >
                            <i class="pi pi-search"></i>
                        </button>
                    </form>
                </div>
                <div
                    class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 2lg:grid-cols-4 gap-3 p-3"
                >
                    <div
                        v-for="med in medications"
                        :key="med.name"
                        class="rounded-lg shadow hover:shadow-md transition-shadow p-6 bg-white text-gray-500 font-medium text-sm"
                    >
                        <p
                            class="text-base text-gray-800 font-semibold overflow-hidden text-ellipsis"
                        >
                            {{ med.name }}
                        </p>
                        <p
                            class="text-gray-500 font-medium text-justify overflow-hidden text-ellipsis whitespace-nowrap"
                        >
                            {{ med.description }}
                        </p>

                        <div class="flex items-center justify-between mt-2">
                            <p
                                class="font-semibold font-poppins text-green-500 text-lg"
                            >
                                ₵ 5
                            </p>
                            <button
                                type="submit"
                                class="whitespace-nowrap py-2 px-4 rounded bg-orange-600 text-white font-medium hover:bg-orange-500"
                            >
                                Add item
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
