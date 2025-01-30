function triggerViewCartGA(orderData) {
    try {
        gtag("event", "view_cart", orderData);
        dataLayer.push({ ecommerce: null });
        dataLayer.push({
            event: "view_cart",
            ecommerce: orderData
        });
    } catch (error) {
        console.error("Error in triggerViewCartGA:", error);
    }
}

function triggerAddToWishlistGA(productData) {
    try {
        gtag("event", "add_to_wishlist", productData);
        dataLayer.push({ ecommerce: null });
        dataLayer.push({
            event: "add_to_wishlist",
            ecommerce: productData
        });
    } catch (error) {
        console.error("Error in triggerAddToWishlistGA:", error);
    }
}

function triggerRemoveFromCartGA(productData) {
    try {
        gtag("event", "remove_from_cart", productData);
        dataLayer.push({ ecommerce: null });
        dataLayer.push({
            event: "remove_from_cart",
            ecommerce: productData
        });
    } catch (error) {
        console.error("Error in triggerRemoveFromCartGA:", error);
    }
}

function triggerBeginCheckoutGA(orderData) {
    try {
        console.log("orderdata", JSON.stringify(orderData));
        alert("hello");
        gtag("event", "begin_checkout", orderData);
        dataLayer.push({ ecommerce: null });
        dataLayer.push({
            event: "begin_checkout",
            ecommerce: orderData
        });
    } catch (error) {
        console.error("Error in triggerBeginCheckoutGA:", error);
    }
}