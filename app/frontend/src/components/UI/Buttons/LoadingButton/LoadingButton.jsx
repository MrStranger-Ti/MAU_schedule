import React from "react";
import ButtonSpinner from "../../../Spinner/ButtonSpinner";
import Button from "../Button/Button";

const LoadingButton = ({children, isLoading, showChildrenOnLoad = true, ...props}) => {
    return (
        <Button disabled={isLoading && true} {...props}>
            {isLoading
                ?
                <React.Fragment>
                    <ButtonSpinner/>
                    {showChildrenOnLoad && children}
                </React.Fragment>
                :
                <React.Fragment>
                    {children}
                </React.Fragment>
            }
        </Button>
    );
};

export default LoadingButton;