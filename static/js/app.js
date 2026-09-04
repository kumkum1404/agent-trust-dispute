async function evaluateTransaction() {

    const agentId =
        document.getElementById("agentId").value;

    const maxSpending =
        Number(
            document.getElementById("maxSpending").value
        );

    const category =
        document.getElementById("category").value;

    const merchant =
        document.getElementById("merchant").value;

    const product =
        document.getElementById("product").value;

    const amount =
        Number(
            document.getElementById("amount").value
        );

    const intent =
        document.getElementById("intent").value;


    const payload = {

        mandate: {

            agent_id: agentId,

            max_spending: maxSpending,

            allowed_categories: [
                category
            ],

            allowed_merchants: [
                merchant
            ],

            expires_at:
                "2026-12-31T23:59:59"
        },

        transaction: {

            transaction_id:
                "web_demo_" +
                Date.now(),

            agent_id: agentId,

            product_name: product,

            category: category,

            merchant_id: merchant,

            amount: amount,

            timestamp:
                new Date().toISOString(),

            user_intent: intent,

            requested_category: category,

            requested_max_price: maxSpending
        }
    };


    try {

        const response = await fetch(
            "/api/evaluate",
            {

                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body:
                    JSON.stringify(payload)
            }
        );


        const data =
            await response.json();


        const action =
            data.security_layer
                .final_decision
                .action;


        const decision =
            document.getElementById(
                "decision"
            );


        decision.innerText =
            action;


        document.getElementById(
            "details"
        ).innerText =
            JSON.stringify(
                data,
                null,
                2
            );

    }

    catch (error) {

        document.getElementById(
            "decision"
        ).innerText =
            "ERROR";

        document.getElementById(
            "details"
        ).innerText =
            error.toString();
    }
}